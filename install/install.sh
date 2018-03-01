#!/usr/bin/env bash

if [[ $EUID -ne 0 ]]; then
   echo "Please run as root"
   exit 1
fi

apt install \
    python-influxdb \
    python-pip

pip install \
    opencv-python
