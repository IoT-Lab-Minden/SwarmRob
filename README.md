# Swarmrob
## Container Orchestration for Robot Applications
Because of the very heterogeneous composition of software and hardware in robotics, the reproduction of experiments is a common problem.
SwarmRob is a python framework that uses container technologies and orchestration to enable the simple sharing of experimental artifacts and improve the reproducibility
in robotics research.

### General Informations
The reproduction of experiments and its results is one of the fundamental problems of robotics. SwarmRob tries to solve it by providing a solution for re-executing and reproducing experiments. The solution allows to run an experiment not only on one robot but also having a cluster of robots run multiple services that communicate with each other. For this purpose, SwarmRob uses container virtualization in combination with an orchestration mechanism that is adapted to the requirements of robotics. The software is oriented along the master-worker-pattern, where a single master manages the experiment together with the participating robots called worker.

### Build Project

- ./build_project.sh

### Start Swarmrob

- Start Daemons
	- swarmrob daemon start

- Initialize Swarm
	- swarmrob master init

- Join Swarm
	- swarmrob worker join $UUIDOFSWARM

### Copyright
Copyright 2018,2019 Aljoscha Pörtner
Copyright 2019 André Kirsch

This file is part of SwarmRob.

SwarmRob is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

SwarmRob is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with SwarmRob.  If not, see <https://www.gnu.org/licenses/>.

