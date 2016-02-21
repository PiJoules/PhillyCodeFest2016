#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import json

from flask import Flask, request
from septanotifier import SeptaNotifier

app = Flask(__name__)


# Root directory
@app.route('/')
def index_route():
    return "Nothing to see here"


@app.route("/data")
def data_route():
    """Get the latest info for the nearest bus."""
    route = request.args.get("route", None)
    direction = request.args.get("direction", None)
    stop_id = request.args.get("stop_id", None)

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
    notifier = SeptaNotifier(int(route), direction, int(stop_id))
    return json.dumps({
        "eta": notifier.eta,
        "arrival_status": notifier.arrival_status,
        "nearest_bus": notifier.next_bus
    }, indent=4)


if __name__ == '__main__':
    app.run(debug=True, port=8080, host="0.0.0.0")
