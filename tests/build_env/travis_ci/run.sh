#!/bin/bash

export PATH=$HOME/.local/bin:$PATH
cd SwarmRob
swarmrob_dummy 
./swarmrob/unittest.sh
sphinx-apidoc -f -o $PWD/swarmrob/docs/source $PWD/swarmrob $PWD/swarmrob/setup.py
travis-sphinx build -n --source=$PWD/swarmrob/docs/source
