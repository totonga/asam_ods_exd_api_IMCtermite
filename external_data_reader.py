"""EXD API implementation for termite raw/dat files"""
import os
from pathlib import Path
import threading
from urllib.parse import urlparse

import grpc
import ods_pb2 as ods
import ods_external_data_pb2 as exd_api
import ods_external_data_pb2_grpc

import IMCtermite


class ExternalDataReader(ods_external_data_pb2_grpc.ExternalDataReader):

    def Open(self, request, context):
        file_path = Path(self.__get_path(request.url))
        if not file_path.is_file():
            raise Exception(f'file "{request.url}" not accessible')

        connection_id = self.__open_file(request)

        rv = exd_api.Handle(uuid=connection_id)
        return rv

    def Close(self, request, context):
        self.__close_file(request)
        return exd_api.Empty()

    def GetStructure(self, request, context):

        if request.suppress_channels or request.suppress_attributes or 0 != len(request.channel_names):
            context.set_code(grpc.StatusCode.UNIMPLEMENTED)
            context.set_details('Method not implemented!')
            raise NotImplementedError('Method not implemented!')

        identifier = self.connection_map[request.handle.uuid]
        channels = self.__get_file(request.handle)

        rv = exd_api.StructureResult(identifier=identifier)
        rv.name = Path(identifier.url).name

        for group_index, channel in enumerate(channels) :

            new_group = exd_api.StructureResult.Group()
            new_group.name = channel["name"]
            new_group.id = group_index
            new_group.total_number_of_channels = 2
            new_group.number_of_rows = len(channel["ydata"])
            new_group.attributes.variables["comment"].string_array.values.append(channel["comment"])
            new_group.attributes.variables["uuid"].string_array.values.append(channel["uuid"])
            new_group.attributes.variables["description"].string_array.values.append(channel["description"])
            new_group.attributes.variables["origin"].string_array.values.append(channel["origin"])

            new_channel = exd_api.StructureResult.Channel()
            new_channel.name = channel["xname"]
            new_channel.id = 0
            new_channel.data_type = ods.DataTypeEnum.DT_DOUBLE
            new_channel.unit_string = channel["xunit"]
            new_group.channels.append(new_channel)

            new_channel = exd_api.StructureResult.Channel()
            new_channel.name = channel["yname"]
            new_channel.id = 1
            new_channel.data_type = ods.DataTypeEnum.DT_DOUBLE
            new_channel.unit_string = channel["yunit"]
            new_group.channels.append(new_channel)

            rv.groups.append(new_group)
            group_index += 1

        return rv

    def GetValues(self, request, context):

        channels = self.__get_file(request.handle)

        if request.group_id < 0 or request.group_id >= len(channels):
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f'Invalid group id {request.group_id}!')
            raise NotImplementedError(f'Invalid group id {request.group_id}!')

        channel = channels[request.group_id]

        nr_of_rows = len(channel["ydata"])
        if request.start >= nr_of_rows:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f'Channel start index {request.start} out of range!')
            raise NotImplementedError(f'Channel start index {request.start} out of range!')

        end_index = request.start + request.limit
        if end_index >= nr_of_rows:
            end_index = nr_of_rows

        rv = exd_api.ValuesResult(id=request.group_id)
        for channel_id in request.channel_ids:
            data = None
            if 0 == channel_id:
                data = channel["xdata"]
            elif 1 == channel_id:
                data = channel["ydata"]
                pass
            else:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details(f'Invalid channel id {channel_id}!')
                raise NotImplementedError(f'Invalid channel id {channel_id}!')

            new_channel_values = exd_api.ValuesResult.ChannelValues()
            new_channel_values.id = channel_id
            new_channel_values.values.data_type = ods.DataTypeEnum.DT_DOUBLE
            new_channel_values.values.double_array.values[:] = data[request.start:end_index]

            rv.channels.append(new_channel_values)

        return rv

    def GetValuesEx(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')
    

    def __init__(self):
        self.connect_count = 0
        self.connection_map = {}
        self.file_map = {}
        self.lock = threading.Lock()

    def __get_id(self, identifier):
        self.connect_count = self.connect_count + 1
        rv = str(self.connect_count)
        self.connection_map[rv] = identifier
        return rv

    def __get_path(self, file_url):
        p = urlparse(file_url)
        final_path = os.path.abspath(os.path.join(p.netloc, p.path))
        return final_path

    def __open_file(self, identifier):
        with self.lock:
            identifier.parameters
            connection_id = self.__get_id(identifier)
            connection_url = self.__get_path(identifier.url)
            if connection_url not in self.file_map:
                file_handle = IMCtermite.imctermite(str(connection_url).encode('utf-8'))
                channels = file_handle.get_channels(True) # we need true to determine length

                self.file_map[connection_url] = { "file" : channels, "ref_count" : 0 }
            self.file_map[connection_url]["ref_count"] = self.file_map[connection_url]["ref_count"] + 1
            return connection_id

    def __get_file(self, handle):
        identifier = self.connection_map[handle.uuid]
        connection_url = self.__get_path(identifier.url)
        return self.file_map[connection_url]["file"]

    def __close_file(self, handle):
        with self.lock:
            identifier = self.connection_map[handle.uuid]
            connection_url = self.__get_path(identifier.url)
            if self.file_map[connection_url]["ref_count"] > 1:
                self.file_map[connection_url]["ref_count"] = self.file_map[connection_url]["ref_count"] - 1
            else:
                #self.file_map[connection_url]["file"].close() # needs some cleanup?
                del self.file_map[connection_url]
