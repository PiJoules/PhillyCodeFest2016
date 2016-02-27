#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script for gettiing the closest bus to a given bus stop.

Will do a lazy check for now of how long it will take for the bus to arrive
getting the direct displacement between the bus and the stop, not (yet)
taking into account the actual distance from the roads taken.

This could be taken care of with the google maps distance matrix api,
though I intend to not depend on that as a primary source.

My first goal is to get a decent way of getting an approximate time of when
the bus will arrived base mostly on the GPS coordinates of where the bus was.
This will allow me to always know where the bus was regardless of any unknown
factors like traffic, detours, accidents, etc.

My second goal will be to predict where the bus acurrently is. This will be
more difficult since it requires me knowing the eactual route of the bus.
This could be done using the google maps api, though I admitentaly (<- probably
spelled incorrectly), have fear of going over API usage limits. My plan to
tackle this problem will be to rely on historical data of paths the bus has
taken at a given time. There is most likely an easier solution to this that
may involve an API other than septa, but I would like to restrct the number of
dependencies this application has.
"""

from __future__ import print_function

import sys

from notifier import SeptaNotifier


def get_args():
    """Standard cmd line arg parser."""
    from argparse import ArgumentParser
    parser = ArgumentParser("Get the closest bus to a stop")

    parser.add_argument("-r", "--route", type=int, required=True,
                        help="Route number")
    parser.add_argument("-d", "--direction", required=True,
                        choices=("northbound", "southbound", "westbound",
                                 "eastbound"),
                        help="Bus direction")
    parser.add_argument("-s", "--stop_id", type=int, required=True,
                        help="Bus stop id. This is meant to be representative "
                        "of the bus stop location and can be swapped with "
                        "the stop lng/lat.")
    parser.add_argument("--working_dir", default="working_dir",
                        help="Working directory to place log files.")

    args = parser.parse_args()
    return args


def main():
    args = get_args()

    route = args.route
    direction = args.direction
    stop_id = args.stop_id
    working_dir = args.working_dir

    notifier = SeptaNotifier(working_dir)
    closest_bus = notifier.closest_bus(route, direction, stop_id)
    print("closest_bus:", closest_bus)

    return 0


if __name__ == "__main__":
    sys.exit(main())

