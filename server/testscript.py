import requests


BASE = "http://www3.septa.org/hackathon/TransitView/"

def collect(route):
    resp = requests.get(BASE, params={"route": route})
    if resp.status_code != 200:
        raise RuntimeError("Could not get json for route {} from '{}'.".format(route, resp.url))
    return resp.json()
