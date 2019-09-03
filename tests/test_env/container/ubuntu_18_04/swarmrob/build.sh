#!/bin/bash
#Copyright 2018,2019 Aljoscha Pörtner
#Copyright 2019 André Kirsch

#This file is part of SwarmRob.

#SwarmRob is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#SwarmRob is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with SwarmRob.  If not, see <https://www.gnu.org/licenses/>.

TWISTED_FOLDER=/opt/Swarmbot
DIST_NAME_FULL=Swarmrob-Full-0.1.tar.gz
PACKAGE_NAME_FULL=swarmrob-full
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $DIR
sudo pip3 install --ignore-installed --upgrade . -r requirements.txt
[ $? -ne 0 ] && echo "Error in pip install !" && exit 1
sudo python3 setup.py sdist

if [ ! -d $TWISTED_FOLDER/simple ]; then
	sudo mkdir -p $TWISTED_FOLDER/simple
fi

sudo rm -R -f  $TWISTED_FOLDER/simple/$PACKAGE_NAME_FULL
sudo mkdir -p $TWISTED_FOLDER/simple/$PACKAGE_NAME_FULL
sudo cp dist/$DIST_NAME_FULL $TWISTED_FOLDER/simple/$PACKAGE_NAME_FULL
