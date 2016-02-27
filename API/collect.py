#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import requests
import sys

from histdata import HistDataManager


class Collector(HistDataManager):
    """Class for collecting data from septa API."""

    # API endpoints
    BUS_URL = "http://www3.septa.org/hackathon/TransitView/{route}"
    STOP_URL = "http://www3.septa.org/hackathon/Stops/{route}"

    def collect_bus_data(self, route):
        """Get the bus data json from the septa api."""
        # Perform get request
        bus_url = self.BUS_URL.format(route=route)
        resp = requests.get(bus_url)

        # Check response
        if resp.status_code != 200:
            raise RuntimeError(
                "Unable to get septa bus data for route {}: {}"
                .format(route, resp.text))

        # Valid response
        self._write_bus_data(route, resp.json())

    def collect_stop_data(self, route):
        """Get the stop data json from the septa api."""
        # Perform get request
        stop_url = self.STOP_URL.format(route=route)
        resp = requests.get(stop_url)

        # Check response
        if resp.status_code != 200:
            raise RuntimeError(
                "Unable to get septa bus data for route {}: {}"
                .format(route, resp.text))

        # Valid response
        self._write_stop_data(route, resp.json())


def get_args():
    """Standard cmd line arg parser."""
    from argparse import ArgumentParser
    parser = ArgumentParser("Get the closest bus to a stop")

    parser.add_argument("-r", "--route", type=int, required=True,
                        help="Route number")
    parser.add_argument("--working_dir", default="working_dir",
                        help="Working directory to place log files.")

    args = parser.parse_args()
    return args


def main():
    args = get_args()

    route = args.route
    working_dir = args.working_dir

    collector = Collector(working_dir)
    collector.collect_bus_data(route)
    collector.collect_stop_data(route)

    return 0


if __name__ == "__main__":
    sys.exit(main())

