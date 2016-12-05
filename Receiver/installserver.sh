#!/bin/bash
receiver_path=/srv/receiver
mkdir $receiver_path
cp receiver.py $receiver_path

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
touch /etc/systemd/system/receiver.service
printf '[Unit]\nDescription=workServer Service\nAfter=rc-local.service\n' >> /etc/systemd/system/receiver.service
printf '[Service]\nWorkingDirectory=%s\n' $workserver_path >> /etc/systemd/system/receiver.service
printf 'ExecStart=/usr/bin/python3 %s/receiver.py\n' $workserver_path >> /etc/systemd/system/receiver.service
printf 'ExecReload=/bin/kill -HUP $MAINPID\nKillMode=process\nRestart=on-failure\n' >> /etc/systemd/system/receiver.service
printf '[Install]\nWantedBy=multi-user.target\nAlias=receiver.service' >> /etc/systemd/system/receiver.service

systemctl start receiver


