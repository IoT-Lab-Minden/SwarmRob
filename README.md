# Copyright 2018,2019 Aljoscha Pörtner
# Copyright 2019 André Kirsch

# This file is part of SwarmRob.

# SwarmRob is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# SwarmRob is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with SwarmRob.  If not, see <https://www.gnu.org/licenses/>.

# Swarmrob
## Container Orchestration for Robot Applications
-----

### Requirements:

- pip >= 9.0.1
    - sudo easy_install pip
    - sudo pip install --uprade pip #Upgrade to the newest version

### Add local python repository and install Swarmbot

On Master (SwarmRob-Full):
- Configure build.sh
            distributeLocally.sh
```
TWISTED_FOLDER=/home/ubuntu/pip_repository/simple #Folder of the repository
DIST_NAME=SwarmRob-0.1.tar.gz #Output of the sdist-command
PACKAGE_NAME=SwarmRob #Packagename
```
- Add lines to ~/.pip/pip.conf
```
[global]
; Extra index to private pypi dependencies
extra-index-url = http://172.20.24.183:8080/simple/
trusted-host = 172.20.24.183
```

- Run distributeLocally.sh in separate terminal
- Run build.sh whenever you want to rebuild and distribute the project

- Run install

[Install]

```
sudo pip install SwarmRob-Full -v

[Reinstall]
```
sudo pip install [--upgrade --force-reinstall --no-deps] SwarmRob-Full

On client (SwarmRob-Worker):

- Add lines to ~/.pip/pip.conf
```
[global]
; Extra index to private pypi dependencies
extra-index-url = http://172.20.24.183:8080/simple/
trusted-host = 172.20.24.183
```

OR

- Run install with params:

sudo pip install --index-url http://172.20.24.183:8080/simple/ --trusted-host 172.20.24.183 --extra-index-url https://pypi.python.org/simple/ --ignore-installed --no-deps --no-cache-dir SwarmRob-Worker

- Run install

[Install]

```
sudo pip install SwarmRob-Worker -v

[Reinstall]
```
sudo pip install [--upgrade --force-reinstall --no-deps] SwarmRob-Worker

### Build Project

- cd src/
- sudo pip install --upgrade -v .

### Build Documentation

- cd doc/
- sudo ./builddoc.sh

### Start Swarmrob

- Start Daemons
	- sudo /etc/init.d/swarmrobns start
	- sudo /etc/init.d/swarmrobd start (swarmrob daemon start)

- Initialize Swarm
	- swarmrob master init --advertise_address $HOST

- Join Swarm
	- swarmrob worker join $UUIDOFSWARM
