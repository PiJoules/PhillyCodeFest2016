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
from bus import Bus, TimeFrame


class HistDataManager(ReaderMixin, WriterMixin):
    """Class for handling data retrieval and storage for the log files."""

    def __init__(self, working_dir):
        super(HistDataManager, self).__init__(working_dir)

    def bus_data(self, route, sort=False):
        """Get list of timeframes of bus objects."""
        # Initialize variables
        bus_files = self._available_bus_files(route, sort=sort)
        read_json = self._read_json
        bus_data = []

        for bus_file in bus_files:
            bus_json = read_json(bus_file)
            if bus_json is not None:
                recv_time = self._date_from_file(bus_file)
                buses = map(lambda x: Bus.from_json(x), bus_json["bus"])
                timeframe = TimeFrame(recv_time, data=buses)
                bus_data.append(timeframe)
        return bus_data

    def latest_bus_data(self, route):
        """Get the latest bus data available."""
        bus_data = self.bus_data(route, sort=True)
        if bus_data:
            return bus_data[-1]
        return []

