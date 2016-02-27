#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Save the file as simple json for now.

Logging hierarchy:
/path/to/working_dir/
- buses/
  - route_number/
    - yyyymmdd_hhmmss.json
- stops/
  - route_number/
    - yyyymmdd_hhmmss.json
"""


from __future__ import print_function

import os
import errno

from datetime import datetime


class WriterMixin(object):
    """Class for logging septa data."""

    def __init__(self, working_dir):
        # Create the dirs
        self.__working_dir = working_dir
        buses_dir = os.path.join(working_dir, "buses")
        stops_dir = os.path.join(working_dir, "stops")
        self.mkdir(buses_dir)
        self.mkdir(stops_dir)

    @staticmethod
    def mkdir(dirname):
        # Create the dirs if not exist.
        try:
            os.makedir(dirname)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise RuntimeError(
                    "Could not create working dir '{}': {}"
                    .format(dirname, e))

    def __write_data(self, data_type, route, json_data):
        """Write json data to a file."""
        # Create the dir if not exist
        working_dir = self.__working_dir
        route_path = os.path.join(working_dir,
                                  "{}/route_{}".format(data_type, route))
        self.mkdir(route_path)

        # Write to json file
        filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"
        file_path = os.path.join(working_dir, filename)
        with open(file_path, "w") as route_file:
            route_file.write(json_data)

    def write_bus_data(self, route, bus_json):
        """Log the bus data number."""
        self.__write_data("buses", route, bus_json)

    def write_stop_data(self, route, stop_json):
        """
        Log the stop data. This should not be done frequently since this
        is static data being recorded.
        """
        self.__write_data("stops", route, stop_json)


class HistDataManager(object):
    """Class for handling data retrieval and storage for the log files."""

    def __init__(self):
        pass

