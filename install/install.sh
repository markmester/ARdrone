#!/usr/bin/env bash

if [[ $EUID -ne 0 ]]; then
   echo "Please run as root"
   exit 1
fi

apt install python3 python3-pip
pip3 install scapy-python3 pyyaml rq