#!/usr/bash
wget https://raw.githubusercontent.com/v2fly/fhs-install-v2ray/master/install-release.sh
sudo bash ./go.sh 
sudo systemctl start v2ray

sudo python3 manage.py migrate
sudo pip3 install -r requirements.txt