#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for holding the writer mixin.
"""


from __future__ import print_function

import os
import json

from datetime import datetime
from base import BaseDataManager


class WriterMixin(BaseDataManager):
    """Class for writing septa data."""

    def __write_data(self, dst_dir, json_data):
        """Write json data to a file."""
        # Create the dir if not exist
        self.mkdir(dst_dir)

        # Write to json file
        filename = datetime.now().strftime(self.DATETIME_FORMAT) + ".json"
        file_path = os.path.join(dst_dir, filename)
        self.__write_json(file_path)

    def __write_json(self, filename, json_data):
        """Write json to a file."""
        with open(filename, "w") as route_file:
            route_file.write(json.dumps(json_data))

    def _write_bus_data(self, route, bus_json):
        """Log the bus data number."""
        dst_dir = os.path.join(self._buses_dir, "route_" + str(route))
        self.__write_data(dst_dir, bus_json)

    def _write_stop_data(self, route, stop_json):
        """
        Log the stop data. This should not be done frequently since this
        is static data being recorded.
        """
        dst_dir = os.path.join(self._stops_dir, "route_" + str(route))
        self.__write_data(dst_dir, stop_json)

    def _write_vector_plot_data(self, route, direction, json_data):
        """Write vector plot json."""
        dst_dir = os.path.join(self._vector_plots_dir, "route_" + str(route))
        self.mkdir(dst_dir)
        dst_filename = os.path.join(dst_dir, direction + ".json")
        self.__write_json(dst_filename, json_data)

