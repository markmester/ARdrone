#!/usr/bin/env bash

# This script to be run on server side i.e. your RPi, run:
trap 'echo oh, I am slain && rm fifo; exit' INT

CLIENT_IP=10.0.1.23
PORT=5000
VIDEO_WIDTH=480
VIDEO_HEIGTH=360

# create fifo
if [ -p fifo ]
then
    rm fifo
fi

mkfifo fifo

# loop until able to connect to client
while true; do
    cat fifo | nc.traditional -u $CLIENT_IP $PORT & raspivid -o fifo -t 0 -w $VIDEO_WIDTH -h $VIDEO_HEIGTH
    sleep 5

    # loop as long as connected to client
    while [ -e /proc/$! ]; do
        echo "Stream running at $CLIENT_IP:$PORT"
        sleep 1
    done
done