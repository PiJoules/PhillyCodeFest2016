#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for holding vector logic.
"""

from __future__ import print_function

import json

from geopy.point import Point
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


def bearing_from_points(start, end):
    """Get the bearing from the points."""
    return bearing(start.latitude, start.longitude,
                   end.latitude, end.longitude)


class Vector(object):
    """Class represnting the velocity of traffic in a given location."""

    __slots__ = ("bearing", "speed", "point")

    def __init__(self, bearing, speed, point):
        self.bearing = bearing
        self.speed = speed
        self.point = point

    def json(self):
        """JSON representation of this type of object."""
        point = self.point
        return {
            "bearing": self.bearing,
            "speed": self.speed,
            "point": {
                "lat": point.latitude,
                "lng": point.longitude
            }
        }

    def __sub__(self, other):
        """Return the distance between 2 vector points."""
        return vincenty(self.point, other.point).meters

    @classmethod
    def from_json(cls, json_str):
        """Create a vector from json string."""
        json_obj = json.loads(json_str)
        return cls.from_dict(json_obj)

    @classmethod
    def from_dict(cls, json_obj):
        """Create a vector from a dict."""
        bearing = float(json_obj["bearing"])
        speed = float(json_obj["speed"])
        point = json_obj["point"]
        point = Point(float(point["lat"]), float(point["lng"]))
        return cls(bearing, speed, point)

    @classmethod
    def from_points(cls, start, end, dt):
        """Create a vector from a start and end point."""
        bearing = bearing_from_points(start, end)
        distance = vincenty(start, end).meters * 1.0
        return cls(bearing, distance / dt, start)


class VectorPlot(object):
    """Class holding the vector of a bus in a given location."""

    def __init__(self, vectors, margin=50):
        self.__vectors = vectors
        self.__margin = margin

    @classmethod
    def from_file(cls, filename, margin=50):
        """Create the plot from a file."""
        with open(filename, "r") as vp_file:
            vectors = json.load(vp_file)
            return cls(map(lambda v: Vector.from_dict(v), vectors),
                       margin=margin)

    def add_vector(self, vector):
        """
        Try to add a vector to the plot if it is not close enough to
        another existing vector.
        """
        vectors = self.__vectors
        margin = self.__margin
        for v in vectors:
            if vector - v < margin:
                break
        else:
            # vector is not close enough to other vectors
            vectors.append(vector)

    def save(self, filename):
        """Save the vector plot in a file."""
        with open(filename, "w") as dst:
            json_obj = [v.json() for v in self.__vectors]
            dst.write(json.dumps(json_obj))

