#!/bin/bash

cd src
if [[ ! -e /tmp/raspi-sapis.py.pid ]]; then
    echo "Starting Raspi-SAPIS..."
    python3 raspi-sapis.py <username>:<password> &
    echo $! > /tmp/raspi-sapis.py.pid
    echo "Raspi-SAPIS has been started with pid "
    cat /tmp/raspi-sapis.py.pid
else
    echo -n "ERROR: Raspi-SAPIS seems to be running with pid "
    cat /tmp/raspi-sapis.py.pid
    echo
fi
