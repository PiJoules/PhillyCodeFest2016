#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for holding reader mixin.
"""

from __future__ import print_function

import os
import json

from base import BaseDataManager


class ReaderMixin(BaseDataManager):
    """Class for reading septa data."""

    def _read_data(self, read_dir, timestamp):
        """Read json data from a file."""
        filename = timestamp.strftime(self.DATETIME_FORMAT)
        file_path = os.path.join(read_dir, filename)
        return self._read_json(file_path)

    def _read_json(self, filename):
        """Read json from a file."""
        try:
            with open(filename, "r") as json_file:
                return json.load(json_file)
        except IOError as e:
            # Return None if problem arrose (like the file not existsing)
            return None

    def _read_bus_data(self, route, timestamp):
        """Read bus json data."""
        read_dir = os.path.join(self._buses_dir, "route_" + str(route))
        return self._read_data(read_dir, timestamp)

    def _read_stop_data(self, route, timestamp):
        """Read stop json data."""
        read_dir = os.path.join(self._stops_dir, "route_" + str(route))
        return self._read_data(read_dir, timestamp)

    def _read_vector_plots_data(self, route, direction):
        """Read the vector plot json."""
        filename = os.path.join(self._vector_plots_dir, "route_" + str(route),
                                direction + ".json")
        return self._read_json(filename)

