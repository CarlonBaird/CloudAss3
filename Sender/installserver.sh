#!/bin/bash
sender_path=/srv/sender
mkdir $sender_path
cp sender.py $sender_path

# install python3-bottle 
apt-get -y update
apt-get -y install python3-bottle

#install pip
apt-get -y install python-setuptools python-dev build-essential
sudo easy_install pip
sudo pip install --upgrade virtualenv

#install azure
pip install azure


# create a service
touch /etc/systemd/system/sender.service
printf '[Unit]\nDescription=workServer Service\nAfter=rc-local.service\n' >> /etc/systemd/system/sender.service
printf '[Service]\nWorkingDirectory=%s\n' $sender_path >> /etc/systemd/system/sender.service
printf 'ExecStart=/usr/bin/python3 %s/sender.py\n' $sender_path >> /etc/systemd/system/sender.service
printf 'ExecReload=/bin/kill -HUP $MAINPID\nKillMode=process\nRestart=on-failure\n' >> /etc/systemd/system/sender.service
printf '[Install]\nWantedBy=multi-user.target\nAlias=sender.service' >> /etc/systemd/system/sender.service

systemctl start sender


