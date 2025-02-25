import IMCtermite
import unittest
import json
import pathlib
import logging
import os


class TestStringMethods(unittest.TestCase):
    log = logging.getLogger(__name__)

    def __get_example_file_path(self, file_name):
        example_file_path = pathlib.Path.joinpath(pathlib.Path(
            __file__).parent.resolve(), '..', 'data', file_name)
        return pathlib.Path(example_file_path).resolve()

    def test_open(self):
        file_path = self.__get_example_file_path('exampleA.raw')
        self.assertTrue(os.path.isfile(file_path))
        print(str(file_path).encode('utf-8'))
        file_handle = IMCtermite.imctermite(str(file_path).encode('utf-8'))
        print(json.dumps(file_handle.get_channels(False), indent=2))
        # we need true to determine length
        channels = file_handle.get_channels(True)
        for channel in channels:
            uuid = channel["uuid"]
            name = channel["name"]
            description = channel["description"]
            origin = channel["origin"]
            comment = channel["comment"]
            xname = channel["xname"]
            xunit = channel["xunit"]
            xlen = len(channel["xdata"])
            yname = channel["yname"]
            yunit = channel["yunit"]
            ylen = len(channel["ydata"])

            self.assertEqual(channel["xdata"][0:4], [0.0])
            self.assertEqual(channel["ydata"][0:4], [-5.121809677944827e+58])
