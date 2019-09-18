#!/usr/bin/env bash

pip3 install /root/swarmrobw
pip3 install /root/swarmrob
pip3 install -r /usr/local/lib/python3.6/dist-packages/swarmrob/requirements.txt
/etc/init.d/docker start
sleep 5s
docker image pull hello-world
#cd /root/test_container && docker build -t tc .

tail -f /dev/null
