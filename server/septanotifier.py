#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test script for getting all the necessary funcitons working.
"""

from __future__ import print_function

import requests

from bs4 import BeautifulSoup
from geopy import Point
from geopy.distance import vincenty
from math import radians, sin, cos, degrees, atan2


BASE = "http://www3.septa.org/hackathon/TransitView/"
KEY = "AIzaSyDNVFgGVENbLNuUP15b4QgnwmBJ3SygKZY"


class SeptaNotifier(object):
    """Class for handling septa api."""

    def __init__(self, route, direction, stop_id):
        self._route = route
        self._direction = direction.lower()
        self._stop_id = stop_id

        # Initialize properties
        self._buses = None
        self._stop_ids = None
        self._stops_dict = None
        self._stops = None
        self._previous_stop = None
        self._next_bus = None
        self._eta = None
        self._arrival_status = None
        self.__nearest_bus_dist_matrix = None

    @property
    def buses(self):
        """The raw json directly from transitview api."""
        if self._buses is None:
            self._buses = self.__transitview_json(self._route)
        return self._buses

    @property
    def stop_ids(self):
        """List of sorted stop ids."""
        if self._stop_ids is None:
            self._stop_ids = self.__parse_bus_stop_ids(self._route,
                                                       self._direction)
        return self._stop_ids

    @property
    def stops_dict(self):
        """Dict mapping stop id => stop dict."""
        if self._stops_dict is None:
            self._stops_dict = self.__stops_dict(self._route)
        return self._stops_dict

    @property
    def stops(self):
        """Sorted list of stops dicts."""
        if self._stops is None:
            self._stops = self.__stop_order(self._route, self._direction)
        return self._stops

    @property
    def current_stop(self):
        """The current stop object from the stop_id given."""
        return self.stops_dict[self._stop_id]

    @property
    def previous_stop(self):
        """Last stop before given one."""
        if self._previous_stop is None:
            current_stop = self._stop_id
            stops = self.stops
            for i in xrange(1, len(stops)):
                if stops[i]["stopid"] == current_stop:
                    self._previous_stop = stops[i - 1]
                    break
            else:
                # Given is the first stop in the schedule
                self._previous_stop = {}
        return self._previous_stop

    @property
    def next_bus(self):
        """The next to arrive bus (actual, not septa)."""
        if self._next_bus is None:
            self._next_bus = self.__bus_data(self._route, self._direction)
        return self._next_bus

    @property
    def eta(self):
        if self._eta is None:
            self._next_bus = self.__bus_data(self._route, self._direction)
        return self._eta

    @property
    def arrival_status(self):
        if self._arrival_status is None:
            arrival_status = self.eta / 300
            if arrival_status > 6:
                arrival_status = 6
            self._arrival_status = arrival_status
        return self._arrival_status

    def __transitview_json(self, route):
        """Get bus locations for a route from septa transitview."""
        resp = requests.get(BASE, params={"route": route})
        if resp.status_code != 200:
            raise RuntimeError("Could not get json for route {} from '{}'.".format(route, resp.url))
        return resp.json()

    def __parse_bus_stop_ids(self, route, direction):
        """
        Parse html at http://www3.septa.org/stops/bus-stop-ids.php
        to get sorted stop_ids.
        """
        # Perform request
        resp = requests.post("http://www3.septa.org/stops/bus-stop-ids.php",
                             data={"Route": route, "Direction": direction})
        if resp.status_code != 200:
            raise RuntimeError("({}) Could not get html from '{}': {}".format(
                resp.status_code, resp.url, resp.text))

        # Parse html
        html_doc = resp.text
        soup = BeautifulSoup(html_doc, 'html.parser')
        stop_ids = soup.find_all("td", **{"class": "bluedata"})

        # First match is most likelt column header ("Stop ID")
        if not stop_ids[0].getText().isdigit():
            del stop_ids[0]

        return map(lambda x: int(x.getText()), stop_ids)

    def __stops_dict(self, route):
        """Get the stops as a dictionary."""
        # Get json from septa
        resp = requests.get("http://www3.septa.org/hackathon/Stops/" + str(route))
        if resp.status_code != 200:
            raise RuntimeError("({}) Could not get json from '{}': {}".format(
                resp.status_code, resp.url, resp.text))

        # Convert the list of dicts to dict mapping stop_id => stop dict
        return {x["stopid"]: x for x in resp.json()}

    def __stop_order(self, route, direction):
        """
        Get the sorted list of stop names and ids by parsing the html
        returned by this url:
        http://www3.septa.org/stops/bus-stop-ids.php

        route:
            Bus route #
        direction:
            Northbound/Southbound/Eastbound/Westbound

        return:
            List of sorted stops returned by
            http://www3.septa.org/hackathon/Stops/44
            and dictionary of stops.
        """
        # Get sorted list of stop ids
        sorted_stop_ids = self.stop_ids

        # Get the sorted list of stop dicts
        stops_dict = self.stops_dict
        stops = [stops_dict[x] for x in sorted_stop_ids if x in stops_dict]
        return stops

    def __bus_data(self, route, direction):
        """
        Get how long it will take for the next bus to reach a given stop.

        - From the stop id, get the lng/lat coords of that stop.
        - Get the bus locations for a certain route.
          - Filter by direction
        - Need to know direction of the bus.

        route:
            Bus route number
        direction:
            Northbound/Southbound/Eastbound/Westbound
        stop_id:
            Unique ID for each bus stop

        return:
            Next bus actual, accounted for real time
        """
        # Check params
        if direction not in ("northbound", "southbound", "eastbound", "westbound"):
            raise RuntimeError(
                """
                The direction provided ({}) is not an allowed direction
                (Northbound/Southbound/Eastbound/Westbound)."""
                .format(direction))

        # Get buses
        resp = requests.get("http://www3.septa.org/hackathon/TransitView/" + str(route))
        if resp.status_code != 200:
            raise RuntimeError("({}) Could not get json from '{}': {}".format(
                resp.status_code, resp.url, resp.text))
        buses = resp.json()["bus"]
        if not buses:
            # No buses are currently on route for this route
            print("No buses are currently on route for this route")
            return {}

        # Filter by direction
        # buses is the wrong buses returned from septa and filtered.
        buses = filter(lambda x: x["Direction"].lower() == direction, buses)
        if not buses:
            # No buses are found in this direction.
            print("No buses are found in this direction.")
            return {}

        """
        Get the approximate time for next bus.
        The next to arrive bus will be the one with shortest distance between
        the provided stop and the previous stop.
        """
        current_stop = self.current_stop
        previous_stop = self.previous_stop
        curr_lat = current_stop["lat"]
        curr_lng = current_stop["lng"]
        prev_lat = prev_lng = None
        if previous_stop:
            prev_lat = previous_stop["lat"]
            prev_lng = previous_stop["lng"]
        stop_coords = (curr_lat, curr_lng)
        prev_stop_coords = (prev_lat, prev_lng)

        def grade(bus):
            """
            The grade will be the distance between the bus and the given stop
            + the distance between the bus and the previous stop. A lower
            grade is better.
            If previous_stop is empty, do not do math for that stop.
            """
            bus_coords = (float(bus["lat"]), float(bus["lng"]))
            d_curr = vincenty(stop_coords, bus_coords).meters
            if previous_stop:
                d_prev = vincenty(prev_stop_coords, bus_coords).meters
            else:
                d_prev = 0
            return d_curr + d_prev

        # The next bus to arrive
        next_bus = min(buses, key=grade)
        return self.__nearest_real_bus(next_bus, curr_lat, curr_lng)

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

    def __nearest_real_bus(self, septa_bus, end_lat, end_lng):
        """Get the real bus from a septa bus."""
        # Get approx dist and time from google maps distance matrix api
        offset_sec = int(septa_bus["Offset_sec"])
        septa_lat = float(septa_bus["lat"])
        septa_lng = float(septa_bus["lng"])
        bus_coords_str = "{},{}".format(septa_lat, septa_lng)
        end_coord_str = "{},{}".format(end_lat, end_lng)
        params = {
            "origins": bus_coords_str,
            "destinations": end_coord_str,
            "key": KEY
        }
        resp = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json", params=params)
        if resp.status_code != 200:
            raise RuntimeError("({}) Could not get json from '{}': {}".format(
                resp.status_code, resp.url, resp.text))

        rows = resp.json()["rows"]
        if not rows:
            raise RuntimeError("No rows found")

        elems = rows[0]["elements"]
        if not elems:
            raise RuntimeError("No elements found")

        sorted_elems = sorted(elems, key=lambda x: x["duration"]["value"])
        nearest_elem = None
        for elem in sorted_elems:
            duration_sec = elem["duration"]["value"]
            if duration_sec > offset_sec:
                # self._eta = duration_sec - offset_sec
                nearest_elem = elem
                break
        else:
            # No buses coming since they all passed the stop.
            raise RuntimeError("No buses coming since they all passed the stop.")

        distance_met = nearest_elem["distance"]["value"]
        duration_sec = nearest_elem["duration"]["value"]
        eta = duration_sec - offset_sec
        self._eta = eta

        # Get real lng, lat coords for bus
        start = Point(septa_lat, septa_lng)
        dist = vincenty(kilometers=distance_met / 1000.0)
        bearing = self.__bearing(septa_lat, septa_lng, end_lat, end_lng)
        dest = dist.destination(point=start, bearing=bearing)
        bus_lat = dest.latitude
        bus_lng = dest.longitude
        return {
            "lat": bus_lat,
            "lng": bus_lng,
            "label": septa_bus["label"],
            "VehicleID": septa_bus["VehicleID"],
            "BlockID": septa_bus["BlockID"],
            "Direction": septa_bus["Direction"],
            "destination": septa_bus["destination"],
            "eta": eta
        }

if __name__ == "__main__":
    import json
    x = SeptaNotifier(33, "NorthBound", 359)
    print(json.dumps({
        "eta": x.eta,
        "arrival_status": x.arrival_status
    }, indent=4))
    print(json.dumps({
        "eta": x.eta,
        "arrival_status": x.arrival_status,
        "nearest_bus": x.next_bus
    }, indent=4))
