# Raspi-SurveillanceAPIServer (SAPIS)

Raspberry Pi Surveillance API Server with basic username:password authentication.

The RaspiSurveillanceServer starts and stops the camerastream and surveillance features via this API server.

## Copyright

Copyright (C) 2021 Denis Meyer

## Prerequisites

### Software

* A set up Raspberry Pi
* Python 3 (as "python3")
* Windows
  * Add Python to PATH variable in environment
* Configure settings.json

## Usage

* Configure src/settings.json
* User/Group: pi/pi

* Start shell
* Run the app via script
  * Edit the start script (at least change the username/password)
  * `./scripts/start.sh`
* Stop the app via script
  * `./scripts/stop.sh`
* Run the app
  * `cd src`
  * `python raspi-sapis.py <username>:<password> [--port 8200]`
  * Stop the app
    * Ctrl-C
