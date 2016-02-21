#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for handling bus bearing.
"""

from __future__ import print_function

import json
import os

from geopy.distance import vincenty
from math import radians, sin, cos, degrees, atan2


class Bearing(object):
    """Class for handling bus bearing."""

    FILE_FORMAT = "bearings/bus_{route}_{direction}.json"

    def __init__(self, bus, direction, route, end_lat, end_lng, bus_range=100):
        """Shut up flake8."""
        self._bus = bus
        self._bus_lat = float(bus["lat"])
        self._bus_lng = float(bus["lng"])
        self._direction = direction.lower()
        self._route = route
        self._end_lat = end_lat
        self._end_lng = end_lng
        self._bus_range = bus_range
        self._bearing = None
        self._passed_stop = None

    @property
    def passed_stop(self):
        """
        Check if this bus passed the stop already (end lat/lng).

        Bus will have passed stop if the bearing of the bus is 
        """
        if self._passed_stop is None:
            pass
        return self._passed_stop

    @property
    def filename(self):
        """File storing the bus data."""
        return self.FILE_FORMAT.format(route=self._route,
                                       direction=self._direction)

    @property
    def __cached_bearing(self):
        """Get the bearing from cache."""
        bus_data = None
        filename = self.filename
        if os.path.isfile(filename):
            with open(filename, "r") as file:
                try:
                    bus_data = json.load(file)
                except ValueError:
                    pass
        return bus_data

    def __bearing(self, start_lat, start_lng, end_lat, end_lng):
        """Get the bearing from start and end points."""
        lat1 = radians(start_lat)
        lat2 = radians(end_lat)

        diff_long = radians(end_lng - start_lng)

        x = sin(diff_long) * cos(lat2)
        y = cos(lat1) * sin(lat2) - (sin(lat1) * cos(lat2) * cos(diff_long))

        initial_bearing = degrees(atan2(x, y))
        compass_bearing = (initial_bearing + 360) % 360
        return compass_bearing

    @property
    def bearing(self):
        """Get the bearing of a bus going in a given direction."""
        if self._bearing is None:
            cached_bearing = self.__cached_bearing
            if cached_bearing is None:
                bearing = self.__get_bearing(self._bus_lat, self._bus_lng,
                                             self._end_lat, self._end_lng)
                self.__save_bus_bearing(self._bus, bearing, self._route,
                                        self._bus_range)
            self._bearing = cached_bearing
        return self._bearing

    def __save_bus_bearing(self, bus, bearing, route, bus_range=100):
        """
        Cache the bus bearing.

        JSON formatted as:
        [
            {
                "lat": float,
                "lng": float
            },
            ...
        ]
        """
        bus_lat = self._bus_lat
        bus_lng = self._bus_lng
        filename = self.filename
        bus_coords = (bus_lat, bus_lng)

        bus_data = []
        if os.path.isfile(filename):
            with open(filename, "r") as file:
                try:
                    bus_data = json.load(file)
                except ValueError:
                    pass

        # Save if the bus isn't within bus_range meters
        # of any other bus.
        def is_in_bus_range(bus):
            lat = bus["lat"]
            lng = bus["lng"]
            return vincenty(bus_coords, (lat, lng)).meters <= bus_range

        for bus in bus_data:
            if not is_in_bus_range(bus):
                # Add bus if not in range
                bus_data.append({
                    "lat": bus_lat,
                    "lng": bus_lng
                })
                with open(filename, "w") as file:
                    file.write(json.dumps(bus_data, indent=4))
                return
