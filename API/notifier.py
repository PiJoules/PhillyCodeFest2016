#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from histdata import HistDataManager


class SeptaNotifier(HistDataManager):
    """Class for managing septa bus locations and arrival times."""

    def __init__(self, working_dir):
        super(SeptaNotifier, self).__init__(working_dir)

    def __stop_location(self, stop_id):
        """Get the lat/lng coords of a stop from its id."""
        # TODO: add logic here
        return (40.008193, -75.211255)

    def closest_bus(self, route, direction, stop_id):
        """Bus closest to the given stop."""
        latest = self.latest_bus_data(route)
        buses = latest.data

        # Retain buses going in same direction.
        buses = filter(lambda x: x.direction == direction, buses)

        # Filter out buses that are heading away from the stop.
        stop_loc = self.__stop_location(stop_id)

        # New location will be where the bus would have been heading
        # towards for the duration of the offset. This will require
        # the traffic velocity of a given location.


        print(map(str, buses))

        return None

