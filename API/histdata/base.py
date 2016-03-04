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


class BaseDataManager(object):
    """Base manager for managing the hist data."""

    DATETIME_FORMAT = "%Y%m%d_%H%M%S"

    def __init__(self, working_dir):
        self.__working_dir = os.path.abspath(working_dir)

        # Create the dirs
        self.mkdir(self._buses_dir)
        self.mkdir(self._stops_dir)
        self.mkdir(self._vector_plots_dir)

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

    @property
    def _vector_plots_dir(self):
        """Dir where the vecotr plots are stored."""
        return os.path.join(self._working_dir, "vector_plots")

    def _available_bus_files(self, route, sort=False):
        """List of available bus json files for this route."""
        # Make the dir if not exist yet
        read_dir = os.path.join(self._buses_dir, "route_" + str(route))
        self.mkdir(read_dir)

        files = os.listdir(read_dir)
        if sort:
            files = sorted(files)
        return map(lambda x: os.path.join(read_dir, x), files)

    def _date_from_file(self, filename):
        """Get a datetime from the filename."""
        date_str = filename[-20:-5]
        return datetime.strptime(date_str, self.DATETIME_FORMAT)

    @staticmethod
    def mkdir(dirname):
        # Create the dirs if not exist.
        try:
            os.makedirs(dirname)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise RuntimeError(
                    "Could not create working dir '{}': {}"
                    .format(dirname, e))

