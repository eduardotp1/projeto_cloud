#!/bin/bash
sudo apt-get -y update
sudo apt-get install -y python3-pip
sudo pip3 install boto3
python3 aps3.py
