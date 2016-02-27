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

from writer import WriterMixin
from reader import ReaderMixin


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

