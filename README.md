# Septa Notifier
Because I don't want to wait 20 minutes for the next bus in the freezing rain when it's hot outside.


## Dependencies
These are required to run the different components of the project.

- server
  - requests (2.9.1)
  - beautifulsoup4 (4.4.1)
  - geopy (1.11.0)
  - flask (0.10.1)


## Setup
The flask server and application as a whole requires a few dependencies that must be installed before running.
These dependencies will be installed via `pip` and isolated in a `virtualenv`.


### Installing tools
- [Instructions for installing pip](https://pip.pypa.io/en/stable/installing/)

To install virtualenv:
```sh
$ pip intsall virtualenv
```

### Installing dependencies
The dependencies will be isolated to the virtualenv so the dependencies are not available globally
and take up space on your computer.

To create and start the virtualenv:
```sh
$ virtualenv septa_venv  # Create the virtualenv
$ source septa_venv/bin/activate  # Activate the virtualenv
```

To install the dependencies:
```sh
(septa_venv) $ pip install -r requirements.txt
```

## Usage
Before starting anything, always make sure you are in the virtualenv by running:
```sh
$ source septa_venv/bin/activate
```
The dependencies are installed here and the app will not work otherwise.

Starting the server:
```sh
(septa_venv) $ python __init__.py
```
This launches a flask server accessible at `127.0.0.1:8080`. The main endpoint that calls the core of the application
is at `127.0.0.1:8080/data` and takes the url parameters `?route=ROUTE_NUMBER&direction=(northbound/southbound/eastbound/westbound)&stop_id=STOP_ID`.

Alternatively, you can run the septa notifier independent of the server:
```sh
(septa_venv) $ python septanotifier.py
```

