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

