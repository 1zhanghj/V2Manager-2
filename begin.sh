#!/bin/bash

# Initialization
sudo python3 manage.py migrate
sudo pip3 install -r requirements.txt