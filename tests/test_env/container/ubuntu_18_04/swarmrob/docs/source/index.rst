.. SwarmRob-Full documentation master file, created by
   sphinx-quickstart on Tue Aug 29 17:36:22 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

SwarmRob
=========================================
Because of the very heterogeneous composition of software and hardware in robotics, the reproduction of experiments is a common problem.
SwarmRob is a python framework that uses container technologies and orchestration to enable the simple sharing of experimental artifacts and improve the reproducibility
in robotics research.

General Informations
-----------------------------------------
The reproduction of experiments and its results is one of the fundamental problems of robotics. SwarmRob tries to solve it by providing a solution for re-executing and reproducing experiments. The solution allows to run an experiment not only on one robot but also having a cluster of robots run multiple services that communicate with each other. For this purpose, SwarmRob uses container virtualization in combination with an orchestration mechanism that is adapted to the requirements of robotics. The software is oriented along the master-worker-pattern, where a single master manages the experiment together with the participating robots called worker (See :numref:`sr_architecture`).

.. _sr_architecture:
.. figure:: _static/images/swarmrob_architecture.png
    :scale: 20%
    :align: center

    The Architecture of SwarmRob - The green cubes represent the worker
    nodes and the red cubes represent the master nodes. Every bounding box
    illustrates a swarm.The outer box illustrates the local network of the laboratory
    and the grey boxes illustrates the repositories where the worker can obtain
    the definition files.

An experiment is described using Docker-like configuration files which can be published using private or public repositories and can be obtained by other researchers. The workflow can be subdivided in two phases: the research phase and the review phase (See :numref:`sr_workflow`).

.. _sr_workflow:
.. figure:: _static/images/workflow.png
    :scale: 40%
    :align: center

    Workflow of SwarmRob - The figure illustrates the research phase (left timeline) and the review phase (right timeline) of the workflow with their
    related subphases.

The research phase is the phase where the experiment is developed and specified by the responsible researchers. Every robot participating in the experiment is specified using a Service Definition File (SDF). The SDF includes the complete functional scope of Docker and should be an executable image of this specific robot. An example of a valid SDF is shown in the following code block.

.. code-block:: dockerfile

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

Afterwards, the researcher can compose the experiment by the defining an experiment definition file (EDF) that references the prior defined SDFs. An EDF is a subset of docker-compose adapted to specific requirements of robotics like the definition of required hardware, e.g. camera, laser scanner etc.. The difference between docker-compose and SwarmRob is that the definition of devices is taken into account within the orchestration and allocation process. An example of a valid EDF is shown in the following code block.

.. code-block:: dockerfile

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

Afterwards, the researchers just need to publish the SDFs and EDFs along with the publication to allow other researchers to get them and reproduce the experiment. As previously described, therefore SwarmRob relies on container virtualization to enable the reproduction of software-intensive multi-robot experiments. A key feature of multi-robot systems is the communicaiton. In order to enable a capsulated and inference-free communication between the robots, SwarmRob makes use of the virtual network feature of Docker based on VXLAN. While the use of container virtualization becomes more common in robotics, especially the networking is a very time-consuming and error-prone procedure. SwarmRob automates this by using a distributed key-value store to spread the correct network configuration to all participating robots. This enables the communication between e.g. ROS nodes via virtual networks on top of the original underlying network. The whole configuration of the swarm is carried out by the software. The researchers only need to initialize a swarm, add the workers and start the swarm.

.. _sr_networking:
.. figure:: _static/images/networking.png
      :scale: 15%
      :align: center

      System and Inter-Robot Network Architecture using Overlay Networks - The Underlay Network represents the physical network connection between
      the hosts, the Intra-Swarm Communication represents the commands and
      information exchanged between the participants of a swarm and the Overlay
      Network is the communication channel used for the communication between
      containerized applications

A good start to connect with SwarmRob is to follow the Getting started guide which you can find :ref:`here <gettingstarted>`.

If you want to have an overview of SwarmRob you can take a look at all the commands :ref:`here <commands>`.

Installation
-----------------------------------------
Informations on how to install SwamRob are available :ref:`here <installation>`.

License
-----------------------------------------
GPL License

    Copyright 2018,2019 Aljoscha Pörtner
    Copyright 2019 André Kirsch

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Dieses Programm ist Freie Software: Sie können es unter den Bedingungen
    der GNU General Public License, wie von der Free Software Foundation,
    Version 3 der Lizenz oder (nach Ihrer Wahl) jeder neueren
    veröffentlichten Version, weiter verteilen und/oder modifizieren.

    Dieses Programm wird in der Hoffnung bereitgestellt, dass es nützlich sein wird, jedoch
    OHNE JEDE GEWÄHR,; sogar ohne die implizite
    Gewähr der MARKTFÄHIGKEIT oder EIGNUNG FÜR EINEN BESTIMMTEN ZWECK.
    Siehe die GNU General Public License für weitere Einzelheiten.

    Sie sollten eine Kopie der GNU General Public License zusammen mit diesem
    Programm erhalten haben. Wenn nicht, siehe <https://www.gnu.org/licenses/>.

Navigation
----------------------------------------

.. toctree::
   :maxdepth: 1

   Installation
   GettingStarted
   FAQ
   Commands
   Changelog
   genindex
   modules
