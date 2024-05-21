# Prepare python to use GRPC interface:
# python -m grpc_tools.protoc --proto_path=proto_src --pyi_out=. --python_out=. --grpc_python_out=. ods.proto ods_external_data.proto
import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/..")

import logging
import pathlib
import unittest

import ods_pb2 as ods
import ods_external_data_pb2 as oed

from external_data_reader import ExternalDataReader
from google.protobuf.json_format import MessageToJson

class TestExdApiEtc(unittest.TestCase):
    log = logging.getLogger(__name__)

    def _get_example_file_path(self, file_name):
        example_file_path = pathlib.Path.joinpath(pathlib.Path(__file__).parent.resolve(), '..', 'data', file_name)
        return pathlib.Path(example_file_path).absolute().resolve().as_uri().replace('///', '//')

    def test_file_EngineSpeed(self):
        service = ExternalDataReader()
        handle = service.Open(oed.Identifier(
            url = self._get_example_file_path('EngineSpeed.dat'),
            parameters = ""), None)
        try:
            structure = service.GetStructure(oed.StructureRequest(handle=handle), None)
            self.log.info(MessageToJson(structure))

            self.assertEqual(structure.name, 'EngineSpeed.dat')
            self.assertEqual(len(structure.groups), 1)
            self.assertEqual(structure.groups[0].number_of_rows, 116888)
            self.assertEqual(len(structure.groups[0].channels), 2)
            self.assertEqual(structure.groups[0].channels[0].data_type, ods.DataTypeEnum.DT_DOUBLE)
            self.assertEqual(structure.groups[0].channels[1].data_type, ods.DataTypeEnum.DT_DOUBLE)

            values = service.GetValues(oed.ValuesRequest(handle=handle,
                                                         group_id=0,
                                                         channel_ids=[0,1],
                                                         start=0,
                                                         limit=4), None)
            self.assertEqual(len(values.channels), 2)
            self.log.info(MessageToJson(values))
            self.assertEqual(values.channels[0].values.data_type, ods.DataTypeEnum.DT_DOUBLE)
            self.assertSequenceEqual(values.channels[0].values.double_array.values, [0.0, 0.1, 0.2, 0.3])
            self.assertEqual(values.channels[1].values.data_type, ods.DataTypeEnum.DT_DOUBLE)
            self.assertSequenceEqual(values.channels[1].values.double_array.values, [0.0, 0.0, 0.0, 0.0])
        finally:
            service.Close(handle, None)

    def test_file_Latitude(self):
        service = ExternalDataReader()
        handle = service.Open(oed.Identifier(
            url = self._get_example_file_path('Latitude.dat'),
            parameters = ""), None)
        try:
            structure = service.GetStructure(oed.StructureRequest(handle=handle), None)
            self.log.info(MessageToJson(structure))

            self.assertEqual(structure.name, 'Latitude.dat')
            self.assertEqual(len(structure.groups), 1)
            self.assertEqual(structure.groups[0].number_of_rows, 11689)
            self.assertEqual(len(structure.groups[0].channels), 2)
            self.assertEqual(structure.groups[0].channels[0].data_type, ods.DataTypeEnum.DT_DOUBLE)
            self.assertEqual(structure.groups[0].channels[1].data_type, ods.DataTypeEnum.DT_DOUBLE)

            values = service.GetValues(oed.ValuesRequest(handle=handle,
                                                         group_id=0,
                                                         channel_ids=[0,1],
                                                         start=0,
                                                         limit=4), None)
            self.assertEqual(len(values.channels), 2)
            self.log.info(MessageToJson(values))
            self.assertEqual(values.channels[0].values.data_type, ods.DataTypeEnum.DT_DOUBLE)
            self.assertSequenceEqual(values.channels[0].values.double_array.values, [0.0, 1.0, 2.0, 3.0])
            self.assertEqual(values.channels[1].values.data_type, ods.DataTypeEnum.DT_DOUBLE)
            self.assertSequenceEqual(values.channels[1].values.double_array.values, [556089856.0, 556089856.0, 556089856.0, 556089856.0])
        finally:
            service.Close(handle, None)

    def test_file_Longitude(self):
        service = ExternalDataReader()
        handle = service.Open(oed.Identifier(
            url = self._get_example_file_path('Longitude.dat'),
            parameters = ""), None)
        try:
            structure = service.GetStructure(oed.StructureRequest(handle=handle), None)
            self.log.info(MessageToJson(structure))

            self.assertEqual(structure.name, 'Longitude.dat')
            self.assertEqual(len(structure.groups), 1)
            self.assertEqual(structure.groups[0].number_of_rows, 11689)
            self.assertEqual(len(structure.groups[0].channels), 2)
            self.assertEqual(structure.groups[0].channels[0].data_type, ods.DataTypeEnum.DT_DOUBLE)
            self.assertEqual(structure.groups[0].channels[1].data_type, ods.DataTypeEnum.DT_DOUBLE)

            values = service.GetValues(oed.ValuesRequest(handle=handle,
                                                         group_id=0,
                                                         channel_ids=[0,1],
                                                         start=0,
                                                         limit=4), None)
            self.assertEqual(len(values.channels), 2)
            self.log.info(MessageToJson(values))
            self.assertEqual(values.channels[0].values.data_type, ods.DataTypeEnum.DT_DOUBLE)
            self.assertSequenceEqual(values.channels[0].values.double_array.values, [0.0, 1.0, 2.0, 3.0])
            self.assertEqual(values.channels[1].values.data_type, ods.DataTypeEnum.DT_DOUBLE)
            self.assertSequenceEqual(values.channels[1].values.double_array.values, [129992016.0, 129992016.0, 129992024.0, 129992024.0])
        finally:
            service.Close(handle, None)

    def test_file_SteeringAngle(self):
        service = ExternalDataReader()
        handle = service.Open(oed.Identifier(
            url = self._get_example_file_path('SteeringAngle.dat'),
            parameters = ""), None)
        try:
            structure = service.GetStructure(oed.StructureRequest(handle=handle), None)
            self.log.info(MessageToJson(structure))

            self.assertEqual(structure.name, 'SteeringAngle.dat')
            self.assertEqual(len(structure.groups), 1)
            self.assertEqual(structure.groups[0].number_of_rows, 116888)
            self.assertEqual(len(structure.groups[0].channels), 2)
            self.assertEqual(structure.groups[0].channels[0].data_type, ods.DataTypeEnum.DT_DOUBLE)
            self.assertEqual(structure.groups[0].channels[1].data_type, ods.DataTypeEnum.DT_DOUBLE)

            values = service.GetValues(oed.ValuesRequest(handle=handle,
                                                         group_id=0,
                                                         channel_ids=[0,1],
                                                         start=0,
                                                         limit=4), None)
            self.assertEqual(len(values.channels), 2)
            self.log.info(MessageToJson(values))
            self.assertEqual(values.channels[0].values.data_type, ods.DataTypeEnum.DT_DOUBLE)
            self.assertSequenceEqual(values.channels[0].values.double_array.values, [0.0, 0.1, 0.2, 0.3])
            self.assertEqual(values.channels[1].values.data_type, ods.DataTypeEnum.DT_DOUBLE)
            self.assertSequenceEqual(values.channels[1].values.double_array.values, [0.0, 0.0, 0.0, 0.0])
        finally:
            service.Close(handle, None)

    def test_file_T_Engine_TC(self):
        service = ExternalDataReader()
        handle = service.Open(oed.Identifier(
            url = self._get_example_file_path('T_Engine_TC.dat'),
            parameters = ""), None)
        try:
            structure = service.GetStructure(oed.StructureRequest(handle=handle), None)
            self.log.info(MessageToJson(structure))

            self.assertEqual(structure.name, 'T_Engine_TC.dat')
            self.assertEqual(len(structure.groups), 1)
            self.assertEqual(structure.groups[0].number_of_rows, 116889)
            self.assertEqual(len(structure.groups[0].channels), 2)
            self.assertEqual(structure.groups[0].channels[0].data_type, ods.DataTypeEnum.DT_DOUBLE)
            self.assertEqual(structure.groups[0].channels[1].data_type, ods.DataTypeEnum.DT_DOUBLE)

            values = service.GetValues(oed.ValuesRequest(handle=handle,
                                                         group_id=0,
                                                         channel_ids=[0,1],
                                                         start=0,
                                                         limit=4), None)
            self.assertEqual(len(values.channels), 2)
            self.log.info(MessageToJson(values))
            self.assertEqual(values.channels[0].values.data_type, ods.DataTypeEnum.DT_DOUBLE)
            self.assertSequenceEqual(values.channels[0].values.double_array.values, [0.0, 0.1, 0.2, 0.3])
            self.assertEqual(values.channels[1].values.data_type, ods.DataTypeEnum.DT_DOUBLE)
            self.assertSequenceEqual(values.channels[1].values.double_array.values, [73.6875, 73.6875, 73.6875, 73.6875])
        finally:
            service.Close(handle, None)

if __name__ == '__main__':
    unittest.main()