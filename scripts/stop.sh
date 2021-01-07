#!/bin/bash

if [[ -e /tmp/raspi-sapis.py.pid ]]; then
    echo "Raspi-SAPIS is running, stopping..."
    kill `cat /tmp/raspi-sapis.py.pid`
    rm /tmp/raspi-sapis.py.pid
    echo "Raspi-SAPIS has been stopped"
else
    echo "Raspi-SAPIS is not running"
fi
