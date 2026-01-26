"""EXD API implementation for termite raw/dat files"""

from __future__ import annotations

import logging
from typing import override

import imctermite
from ods_exd_api_box import ExdFileInterface, exd_api, ods, serve_plugin

# pylint: disable=no-member


class ExternalDataFile(ExdFileInterface):
    """Class for handling for NI tdms files."""

    @classmethod
    @override
    def create(cls, file_path: str, parameters: str) -> ExdFileInterface:
        """Factory method to create a file handler instance."""
        return cls(file_path, parameters)

    @override
    def __init__(self, file_path: str, parameters: str = ""):
        self.file_path: str = file_path
        self.parameters: str = parameters
        self.file_handle = imctermite.imctermite(str(file_path).encode("utf-8"))

    @override
    def close(self):
        if self.file_handle is not None:
            del self.file_handle
            self.file_handle = None

    @override
    def fill_structure(self, structure: exd_api.StructureResult) -> None:
        logging.info("fill_structure: Called")

        channels = self.file_handle.get_channels(True)

        for group_index, channel in enumerate(channels):

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

            structure.groups.append(new_group)
            group_index += 1

    @override
    def get_values(self, request: exd_api.ValuesRequest) -> exd_api.ValuesResult:

        logging.info("GetValues: Called")
        channels = self.file_handle.get_channels(True)

        if request.group_id < 0 or request.group_id >= len(channels):
            raise ValueError(f"Invalid group id {request.group_id}!")

        channel = channels[request.group_id]

        nr_of_rows = len(channel["ydata"])
        if request.start >= nr_of_rows:
            raise ValueError(f"Channel start index {request.start} out of range!")

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
                raise ValueError(f"Invalid channel id {channel_id}!")

            new_channel_values = exd_api.ValuesResult.ChannelValues()
            new_channel_values.id = channel_id
            new_channel_values.values.data_type = ods.DataTypeEnum.DT_DOUBLE
            new_channel_values.values.double_array.values[:] = data[request.start : end_index]

            rv.channels.append(new_channel_values)

        return rv


if __name__ == "__main__":
    serve_plugin("IMC-TERMITE", ExternalDataFile.create, ["*.dat", "*.raw"])
