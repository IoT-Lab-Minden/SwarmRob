# Swarmrob ![travis_ci](https://travis-ci.com/AljoschaP/SwarmRob.svg?token=gbhG8z3VZ5gzPsveAuLR&branch=master)
<p align="center"> 
<img src="https://github.com/IoT-Lab-Minden/SwarmRob/raw/gh-pages/_static/images/SwarmRob_Main_Logo.png" alt="SwarmRob Logo" width="193" height="212">
</p>

## Container Orchestration for Robot Applications
Because of the very heterogeneous composition of software and hardware in robotics, the reproduction of experiments is a common problem.
SwarmRob is a python framework that uses container technologies and orchestration to enable the simple sharing of experimental artifacts and improve the reproducibility
in robotics research.

### General Informations
The reproduction of experiments is one of the fundamental problems of robotics research. SwarmRob tries to solve it by providing a solution to support the re-execution and reproduction of experiments. The solution simplifies the execution of experiments on a cluster of robots with multiple services communicating with each other. For this purpose, SwarmRob uses container virtualization in combination with an orchestration mechanism that is adapted to the requirements of robotics. The software is oriented along the master-worker-pattern. A single master manages the experiment and allocates the services to the participating robots called worker.

<p align="center"> 
<img src="https://github.com/IoT-Lab-Minden/SwarmRob/raw/gh-pages/_static/images/swarmrob_architecture.png" alt="SwarmRob Architecture" width="421" height="288">
</p>

*The Architecture of SwarmRob - The green cubes represent the worker nodes and the red cubes represent the master nodes. Every bounding box illustrates a swarm.The outer box illustrates the local network of the laboratory and the grey boxes illustrates the repositories where the worker can obtain the definition files.*

An experiment is described using Docker-like configuration files which can be published using private or public repositories and can be obtained by other researchers. The workflow can be subdivided in two phases: the research phase and the review phase.

![Workflow](https://github.com/IoT-Lab-Minden/SwarmRob/raw/gh-pages/_static/images/workflow.png)
*Workflow of SwarmRob - The figure illustrates the research phase (left timeline) and the review phase (right timeline) of the workflow with their related subphases.*

The research phase is the phase where the experiment is developed and specified by the responsible researchers. Every robot participating in the experiment is specified using a Service Definition File (SDF). The SDF includes the complete functional scope of Docker and should be an executable image of this specific robot. An example of a valid SDF is shown in the following code block.

```
FROM iotlab/indigo
# Initialize the catkin workspace
USER ros
WORKDIR /home/ros/src
RUN /usr/bin/python /opt/ros/indigo/bin/
catkin_init_workspace
RUN git clone --recursive https://gitlab/repository/
ROSMaster.git -b master
WORKDIR /home/ros
# Build the catkin workspace
RUN /opt/ros/indigo/bin/catkin_make
#...
ENTRYPOINT ["/home/ros/startup.sh"]
```

Afterwards, the researcher can compose the experiment by defining an experiment definition file (EDF) that references the prior defined SDFs. An EDF is a subset of docker-compose adapted to specific requirements of robotics like the definition of required hardware, e.g. camera, laser scanner etc.. The difference between docker-compose and SwarmRob is that the definition of devices is taken into account within the orchestration and allocation process. An example of a valid EDF is shown in the following code block.

```
services:
    rosmaster:
      #Specifies the location of the image
      image: repository:5000/ros-master
      environment:
        - ROS_IP=hm_rosmaster_1
    camera:
      image: repository:5000/ros-smart-camera
      #Specifies service-specific environment variables
      environment:
        - ROS_URI=http://rosmaster_1:11311
        - CAMERA_NAME=Cam
      #Specifies the cross-service dependencies
      depends_on:
        - "rosmaster"
      #Specifies the required devices
      devices:
        - "/dev/video0:/dev/video0"
```

Afterwards, the researchers just need to publish the SDFs and EDFs along with the publication to allow other researchers to get them and reproduce the experiment. As previously described, therefore SwarmRob relies on container virtualization to enable the reproduction of software-intensive multi-robot experiments. A key feature of multi-robot systems is the communicaiton. In order to enable a capsulated and inference-free communication between the robots, SwarmRob makes use of the virtual network feature of Docker based on VXLAN. While the use of container virtualization becomes more common in robotics, especially the networking is a very time-consuming and error-prone procedure. SwarmRob automates this by using a distributed key-value store to spread the correct network configuration to all participating robots. This enables the communication between e.g. ROS nodes via virtual networks on top of the original underlying network. The whole configuration of the swarm is carried out by the software. The researchers only need to initialize a swarm, add the workers and start the swarm.
<p align="center"> 
<img src="https://github.com/IoT-Lab-Minden/SwarmRob/raw/gh-pages/_static/images/networking.png" alt="Networking" width="402" height="370">
</p>

*System and Inter-Robot Network Architecture using Overlay Networks - The Underlay Network represents the physical network connection between the hosts, the Intra-Swarm Communication represents the commands and information exchanged between the participants of a swarm and the Overlay Network is the communication channel used for the communication between containerized applications*

More in-depth information can be found in the publication:

> A. Pörtner, M. Hoffmann, S. Zug, and M. König, “SwarmRob: A Toolkit for Reproducibility and Sharing of Experimental Artifacts in Robotics Research,” in 2018 IEEE International Conference on Systems, Man, and Cybernetics (SMC), 2018, p. 325–332. 

A good start to connect with SwarmRob is to follow the [Getting started](https://iot-lab-minden.github.io/SwarmRob/).

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

