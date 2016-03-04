#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from histdata import HistDataManager
from geopy.distance import vincenty
from math import radians, sin, cos, degrees, atan2


def bearing(start_lat, start_lng, end_lat, end_lng):
    """Get the bearing from start and end points."""
    lat1 = radians(start_lat)
    lat2 = radians(end_lat)

    diff_long = radians(end_lng - start_lng)

    x = sin(diff_long) * cos(lat2)
    y = cos(lat1) * sin(lat2) - (sin(lat1) * cos(lat2) * cos(diff_long))

    initial_bearing = degrees(atan2(x, y))
    compass_bearing = (initial_bearing + 360) % 360
    return compass_bearing


def bus_bearing(start_bus, end_bus):
    """Get the bearing of a bus from its start and end points."""
    return bearing(start_bus.lat, start_bus.lng, end_bus.lat, end_bus.lng)


class Vector(object):
    """Class representing averagevelocity of traffic."""

    __slots__ = ("bearing", "speed", "location")

    def __init__(self, bearing, speed, location):
        self.bearing = bearing
        self.speed = speed
        self.location = location  # (lat, lng)


class VectorPlot(object):
    """Vector plot representing the velocity of traffic in a given location."""

    def __init__(self, vectors, margin=100):
        """
        vectors:
            List of vector objects.
        margin:
            The max distance (in meters) between 2 locations for them to be
            considered the same.
        """
        self.__vectors = vectors
        self.__margin = margin

    def get_velocity(self, lat, lng):
        """Get the velocity of a given location."""
        margin = self.__margin
        for vector in self.__vectors:
            if vincenty((lat, lng), vector.location).meters < margin:
                return vector
        return None

    def add_vector(self, vector):
        """Add a vector to the plot."""
        self.__vectors.append(vector)

    def save(self):
        """Save the plot."""
        pass


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

