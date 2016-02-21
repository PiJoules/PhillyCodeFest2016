#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script for collecting data from septa buses periodically.
"""

from __future__ import print_function

import sys
import requests
import os
import errno

from datetime import datetime

# Base api url
BASE = "http://www3.septa.org/hackathon/TransitView/"


def collect(route):
    """Collect json form septa api as plain text."""
    resp = requests.get(BASE, params={"route": route})
    if resp.status_code != 200:
        print("Unable to get json for route {} from '{}'".format(route, resp.url), file=sys.stderr)
        return None
    else:
        return resp.text


def get_args():
    """Parse command line arguments."""
    from argparse import ArgumentParser
    parser = ArgumentParser("Septa bus logger")
    parser.add_argument("--route", type=int, required=True,
                        help="Bus route number")
    parser.add_argument("--working_dir", required=True,
                        help="Directory where the log will be placed.")
    return parser.parse_args()


def main():
    args = get_args()

    # Format filename
    working_dir = args.working_dir
    route = args.route
    filename = "route_{}_{}.json".format(route, datetime.now().strftime("%Y%m%d_%H%M%S"))
    filepath = os.path.join(working_dir, filename)

    # Create working dir if not exist
    try:
        os.makedirs(working_dir)
    except OSError as err:
        if err.errno != errno.EEXIST:
            print("Could not create dir '{}': {}".format(working_dir, err),
                  file=sys.stderr)
            return 1

    with open(filepath, "w") as dst:
        septa_json = collect(route)
        if septa_json is None:
            return 1
        dst.write(septa_json)

    return 0


if __name__ == "__main__":
    sys.exit(main())
