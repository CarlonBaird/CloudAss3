#!/bin/bash
workserver_path=/srv/workserver
mkdir $workserver_path
cp workserver.py $workserver_path

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
touch /etc/systemd/system/workserver.service
printf '[Unit]\nDescription=workServer Service\nAfter=rc-local.service\n' >> /etc/systemd/system/workserver.service
printf '[Service]\nWorkingDirectory=%s\n' $workserver_path >> /etc/systemd/system/workserver.service
printf 'ExecStart=/usr/bin/python3 %s/workserver.py\n' $workserver_path >> /etc/systemd/system/workserver.service
printf 'ExecReload=/bin/kill -HUP $MAINPID\nKillMode=process\nRestart=on-failure\n' >> /etc/systemd/system/workserver.service
printf '[Install]\nWantedBy=multi-user.target\nAlias=workserver.service' >> /etc/systemd/system/workserver.service

systemctl start workserver


