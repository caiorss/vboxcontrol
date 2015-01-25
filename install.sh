#!/bin/bash
mkdir -p ~/lib
cp libvbox.py ~/lib
cp vboxcontrol.py ~/bin

sudo cp vboxservice.sh /etc/init.d/
sudo update-rc.d vboxservice  defaults 99
