#!/bin/bash

TWISTED_FOLDER=/opt/Swarmbot
DIST_NAME_WORKER=Swarmrob-Worker-0.1.tar.gz
PACKAGE_NAME_WORKER=swarmrob-worker
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $DIR
sudo pip3 install --ignore-installed --upgrade . -r requirements.txt
[ $? -ne 0 ] && echo "Error in pip install !" && exit 1
sudo python3 setup.py sdist
#./scripts/install_swarmrob_worker_service.sh

if [ ! -d $TWISTED_FOLDER/simple ]; then
	sudo mkdir -p $TWISTED_FOLDER/simple
fi

sudo rm -R -f $TWISTED_FOLDER/simple/$PACKAGE_NAME_WORKER
sudo mkdir -p $TWISTED_FOLDER/simple/$PACKAGE_NAME_WORKER
sudo cp dist/$DIST_NAME_WORKER $TWISTED_FOLDER/simple/$PACKAGE_NAME_WORKER
