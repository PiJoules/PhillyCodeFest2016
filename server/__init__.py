#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import json
import time

from flask import Flask, request, redirect
from septanotifier import SeptaNotifier

app = Flask(__name__)


# Root directory
@app.route('/')
def index_route():
    return "Nothing to see here"


@app.route("/data_real")
def data_real_route():
    # Redirect to test
    return redirect("/data_test")

    """Get the latest info for the nearest bus."""
    route = request.args.get("route", None)
    direction = request.args.get("direction", None)
    stop_id = request.args.get("stop_id", None)
    user_offset = request.args.get("user_offset", None)

    # Check params
    if route is None:
        return json.dumps({
            "error": 400,
            "message": "route not provided"
        }, indent=4)
    if direction is None:
        return json.dumps({
            "error": 400,
            "message": "direction not provided"
        }, indent=4)
    if stop_id is None:
        return json.dumps({
            "error": 400,
            "message": "stop_id not provided"
        }, indent=4)

    # Create notifier
    direction = direction.lower()
    try:
        notifier = SeptaNotifier(int(route), direction, int(stop_id),
                                 user_offset=user_offset)
    except Exception as e:
        return json.dumps({
            "error": 400,
            "message": str(e)
        }, indent=4)
    return json.dumps({
        "eta": notifier.eta,
        "arrival_status": notifier.arrival_status,
        "nearest_bus": notifier.next_bus
    }, indent=4)


@app.route("/data")
def data_route():
    """Get the latest info for the nearest bus."""
    route = request.args.get("route", None)
    direction = request.args.get("direction", None)
    stop_id = request.args.get("stop_id", None)
    user_offset = request.args.get("user_offset", None)

    # Check params
    if route is None:
        return json.dumps({
            "error": 400,
            "message": "route not provided"
        }, indent=4)
    if direction is None:
        return json.dumps({
            "error": 400,
            "message": "direction not provided"
        }, indent=4)
    if stop_id is None:
        return json.dumps({
            "error": 400,
            "message": "stop_id not provided"
        }, indent=4)

    # Create notifier
    direction = direction.lower()
    try:
        notifier = SeptaNotifier(int(route), direction, int(stop_id),
                                 user_offset=user_offset)
    except Exception as e:
        return json.dumps({
            "error": 400,
            "message": str(e)
        }, indent=4)
    return json.dumps({
        "eta": notifier.eta,
        "arrival_status": notifier.arrival_status,
        "nearest_bus": notifier.next_bus
    }, indent=4)


@app.route("/data_test")
def data_test_route():
    eta = (-1 * int(time.time()) % 2100)
    arrival_status = min(eta / 300, 6)
    bus_lat = 100
    bus_lng = 100
    septa_bus = {
        "lat": "39.992718",
        "lng": "-75.168159",
        "label": "7412",
        "VehicleID": "7412",
        "BlockID": "5152",
        "Direction": "SouthBound",
        "destination": "Penn`s Landing",
        "Offset": "1",
        "Offset_sec": "31"
    }

    return json.dumps({
        "arrival_status": arrival_status,
        "eta": eta,
        "nearest_bus": {
            "lat": bus_lat,
            "lng": bus_lng,
            "label": septa_bus["label"],
            "VehicleID": septa_bus["VehicleID"],
            "BlockID": septa_bus["BlockID"],
            "Direction": septa_bus["Direction"],
            "destination": septa_bus["destination"],
            "eta": eta
        }
    }, indent=4)


if __name__ == '__main__':
    app.run(debug=True, port=8080, host="0.0.0.0")
