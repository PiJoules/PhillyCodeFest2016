#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from histdata import HistDataManager


class SeptaNotifier(HistDataManager):
    """Class for managing septa bus locations and arrival times."""

    def __init__(self, working_dir):
        super(SeptaNotifier, self).__init__(working_dir)

    def closest_bus(self, route, direction, stop_id):
        """Bus closest to the given stop."""
        print("latest_bus_data:", self.latest_bus_data(route))
        return None

