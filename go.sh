#!/usr/bash
sudo bash <(curl https://raw.githubusercontent.com/v2fly/fhs-install-v2ray/master/install-release.sh)
sudo systemctl start v2ray

sudo python3 manage.py migrate
sudo pip3 install -r requirements.txt