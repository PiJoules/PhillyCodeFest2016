#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function


class Bus(object):
    """Class representing the bus."""

    __slots__ = ("lat", "lng", "id", "direction", "offset")

    def __init__(self, lat, lng, vehicle_id, direction, offset):
        self.lat = lat
        self.lng = lng
        self.id = vehicle_id
        self.direction = direction
        self.offset = offset  # seconds

    @classmethod
    def from_json(cls, bus_json):
        """Create Bus from json provided by septa API."""
        return cls(float(bus_json["lat"]),
                   float(bus_json["lng"]),
                   int(bus_json["VehicleID"]),
                   bus_json["Direction"].lower(),
                   int(bus_json["Offset_sec"]))

    def __str__(self):
        return str({x: getattr(self, x) for x in self.__slots__})

    def __eq__(self, other):
        """Buses are the same if they have the same id."""
        return self.id == other.id

    def __hash__(self):
        """A bus is identified by it's id, lat, lng, and direction."""
        return hash((self.id, self.lat, self.lng, self.direction))


class TimeFrame(object):
    """A container representing an instance of time."""

    def __init__(self, t, data=None):
        self.__time = t
        self.__data = data

    @property
    def datetime(self):
        return self.__time

    @property
    def data(self):
        return self.__data

    def __contains__(self, item):
        return item in self.__data

    def __sub__(self, other):
        return self.datetime - other.datetime

    def __str__(self):
        return str({"datetime": self.datetime, "data": self.data})

