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
import json

from datetime import datetime


class BaseDataManager(object):
    """Base manager for managing the hist data."""

    DATETIME_FORMAT = "%Y%m%d_%H%M%S"

    def __init__(self, working_dir):
        self.__working_dir = os.path.abspath(working_dir)

        # Create the dirs
        self.mkdir(self._buses_dir)
        self.mkdir(self._stops_dir)

    @property
    def _working_dir(self):
        """Root dir where all the files will be logged."""
        return self.__working_dir

    @property
    def _buses_dir(self):
        """Dir where the bus data will be logged."""
        return os.path.join(self._working_dir, "buses")

    @property
    def _stops_dir(self):
        """Dir where the stop data will be logged."""
        return os.path.join(self._working_dir, "stops")

    def _available_bus_data(self, route, sort=False):
        """List of available bus json files for this route."""
        read_dir = os.path.join(self._buses_dir, "route_" + str(route))
        files = os.listdir(read_dir)
        if sort:
            files = sorted(files)
        return map(lambda x: os.path.join(read_dir, x), files)

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


class WriterMixin(BaseDataManager):
    """Class for writing septa data."""

    def __write_data(self, dst_dir, json_data):
        """Write json data to a file."""
        # Create the dir if not exist
        self.mkdir(dst_dir)

        # Write to json file
        filename = datetime.now().strftime(self.DATETIME_FORMAT) + ".json"
        file_path = os.path.join(dst_dir, filename)
        with open(file_path, "w") as route_file:
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


class HistDataManager(ReaderMixin, WriterMixin):
    """Class for handling data retrieval and storage for the log files."""

    def __init__(self, working_dir):
        super(HistDataManager, self).__init__(working_dir)

    def latest_bus_data(self, route):
        """Get the latest bus data available."""
        bus_files = self._available_bus_data(route, sort=True)
        if bus_files:
            return self._read_json(bus_files[-1])["bus"]
        return None

