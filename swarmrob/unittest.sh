#!/bin/bash
echo Starting swarmrob_dummy
swarmrob_dummy
sleep 5
echo Running unittests
python3 -m unittest discover swarmrob
echo Finished
