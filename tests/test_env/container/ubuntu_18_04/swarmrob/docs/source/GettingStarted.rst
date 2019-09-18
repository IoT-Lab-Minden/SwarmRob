.. _gettingstarted:
Getting started
================
To follow the next steps you should have the full version of SwarmRob installed. If you haven't done this already, make sure to install SwarmRob first. You can find the instructions on how to install SwarmRob :ref:`here <installation>`.

Start the daemon
----------------
SwarmRob uses a daemon to always be reachable from other SwarmRob nodes. You can communicate with this daemon via the command line. To do this you first need to start the daemon itself. Execute the following command to start the SwarmRob daemon::

	sudo swarmrob daemon start

Initialize a swarm
----------------
Since the daemon is now running you can initialize your first swarm. A swarm can only be initialized using the full version of SwarmRob because the node you run this command on will become the master of th swarm. The following command will initialize a new swarm::

	sudo swarmrob master init --swarm_uuid my_swarm

With the option ``--swarm_uuid`` you can give your swarm a uuid. It is possible to omit this option. SwarmRob then will automatically assign a uuid but if you have to use a specific uuid or have to write all commands by hand it is recommended to use the option.

Join the swarm
----------------
The command to join a swarm will be printed out by the previously executed command. It should have the following form::

	sudo swarmrob worker join --uuid my_swarm@$IP_ADDRESS

The ``$IP_ADDRESS`` has to be replaced with the ip address of your current system. Note that if you want to join a swarm from a system where only the worker version is installed you have to swap the command ``swarmrob`` to ``swarmrob-worker``. It is possible to have a worker node and a master node running on the same system for easy testing purposes.

To check if the worker has been registered successfully you can execute the following command::

	sudo swarmrob master swarm_status

It shows you a list of worker nodes that are registered at this swarm. In this case you should see one worker node.

Create an EDF
----------------
To start a swarm you need to have a Container Definition File (short CDF) and an Experiment Definition File (short EDF). A CDF describes a service that can be executed by a worker node. CDFs are simply just Dockerfiles. This means you can execute every Dockerfile using SwarmRob. EDFs are similar to the Compose-Files you may know from Docker. In this example we use the ``hello-world`` example from Docker and write an EDF to execute the programm on our worker.

First create a new file called ``my_edf.yaml``. Then copy the following content into the file::

	version: '3'
	services: 
	 my_service:
	  image: hello-world

This EDF describes a service with the name ``my_service`` that should run the image ``hello-world``. If you want to you can run more services. You can do so by adding more services to the EDF. An example with two services would look like this::

	version: '3'
	services: 
	 my_service:
	  image: hello-world
	 my_service_2:
	  image: hello-world

At last you can save your file.

Start the swarm
----------------
We are ready to run our services. Execute the following command to start the swarm::

	sudo swarmrob master start_swarm --swarm_uuid my_swarm --compose_file my_edf.yaml

When you have started your swarm you can check the status of it again using this command::

	sudo swarmrob master swarm_status

You will see that there has been one service assigned. But you may also see that it is not running. But don't worry it has already been executed successfully. To see that the service has exited you can execute the following command::

	sudo swarmrob master worker_status --worker_uuid $WORKER_UUID

To execute the command replace the ``$WORKER_UUID`` with an actual worker uuid. You can look up the worker uuid from your worker node in the output of the status command you executed before. When you have replaced the worker uuid and executed the command you will see ``exited`` in the status column of the Service Status List.

Congratulations! You now have successfully started your first swarm and know the basics of SwarmRob. If you want to learn more about the commands you can use you can take a look at the :ref:`commands page <commands>`.
