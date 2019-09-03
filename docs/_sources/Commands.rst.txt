.. _commands:

Commands
================
Every command you can use starts with either ``swarmrob`` or ``swarmrob-worker``. Which of the one you have to use depends on which version of SwarmRob you have installed. If you have installed the full version you have to use the command ``swarmrob`` and if you have the worker version installed you have to use ``swarmrob-worker``. The examples on this page use the command ``swarmrob`` but work with both commands unless stated otherwise.

SwarmRob uses the three different subcommands master_, worker_ and daemon_ to distinguish between the three different parts of the programm.

**swarmrob check**
	There is also a fourth command that checks if all requirements have been installed correctly and installs them if they haven't been installed already.

Example:
   >>> swarmrob check

**swarmrob help**
	Note that with every command (including ``swarmrob``, ``master``, ``worker`` and ``daemon``) you can always use the help command to get a list of all possible subcommands.

Parameters:
   - -v	[--verbose] : Every command has the ``verbose`` parameter to print more detailed logs *(optional)*

Example:
   >>> swarmrob help
   >>> swarmrob master help
   >>> swarmrob worker help
   >>> swarmrob daemon help

master
----------------
To use the master commands you need to have the full version of SwarmRob installed. They are used to create and manage a swarm.

**swarmrob master init**
	The ``init`` command initializes a new swarm and nominates this node to be the master node of the swarm. Note that only one swarm can be created on one instance of the SwarmRob daemon.

Parameters:
   - -a	[--advertise_address] : IPv4-Address of the master node *(optional)*
   - -i	[--interface] : Interface the command uses to communicate with the daemon *(optional)*
   - -u	[--swarm_uuid] : UUID of the new swarm *(optional)*

Example:
   >>> swarmrob master init -u my_swarm

**swarmrob master list**
	The ``list`` command lists some information about the swarm.

Parameters:
   - -i	[--interface] : Interface the command uses to communicate with the daemon *(optional)*

Example:
   >>> swarmrob master list -i lo

**swarmrob master swarm_status**
	The ``swarm_status`` command prints more informations about the swarm.

Parameters:
   - -i	[--interface] : Interface the command uses to communicate with the daemon *(optional)*

Example:
   >>> swarmrob master swarm_status -i lo

**swarmrob master worker_status**
	The ``worker_status`` command prints more informations of a specific worker in the swarm.

Parameters:
   - -u	[--worker_uuid] : UUID of the worker
   - -i	[--interface] : Interface the command uses to communicate with the daemon *(optional)*

Example:
   >>> swarmrob master worker_status -u ab4f3466c1ed45b3bc78caa38b2ee489

**swarmrob master start_swarm**
	The ``start_swarm`` command executes an EDF and starts its described services on the workers.

Parameters:
   - -u	[--swarm_uuid] : UUID of the new swarm
   - -c	[--compose_file] : EDF that should be executed
   - -i	[--interface] : Interface the command uses to communicate with the daemon *(optional)*
   - -l	[--log_identifier] : Identification string to use for the log file *(optional)*
   - -f	[--log_folder] : Log folder to save the log in *(optional)*

Example:
   >>> swarmrob master start_swarm -u my_swarm -c my_edf.yaml

worker
----------------
The ``worker`` subcommand is used to handle all things related to the worker on the current system.

**swarmrob worker join**
	The ``join`` command lets you add a worker to a swarm.

Parameters:
   - -u	[--uuid] : UUID of the swarm that should be joined
   - -i	[--interface] : Interface the command uses to communicate with the daemon *(optional)*

Example:
   >>> swarmrob worker join -u my_swarm@127.0.0.1

**swarmrob worker leave**
	The ``leave`` command allows you to remove this worker from a swarm. Note that the worker will stop all services that have been running in this swarm.

Parameters:
   - -u	[--uuid] : UUID of the swarm that should be left
   - -w [--worker_uuid] : UUID of the worker that should leave the swarm
   - -i	[--interface] : Interface the command uses to communicate with the daemon *(optional)*

Example:
   >>> swarmrob worker leave -u my_swarm@127.0.0.1 -w ab4f3466c1ed45b3bc78caa38b2ee489

**swarmrob worker status**
	The ``status`` command prints some information about the current worker.

Parameters:
   - -i	[--interface] : Interface the command uses to communicate with the daemon *(optional)*

Example:
   >>> swarmrob worker info -i lo

daemon
----------------
The daemon makes sure that the current node can be reached by other nodes.

**swamrob daemon start**
	The ``start`` command starts the SwarmRob daemon.

Parameters:
   - -i	[--interface] : Interface the daemon should use to communicate *(optional)*

Example:
   >>> swarmrob daemon start -i lo

**swamrob daemon status**
	The ``status`` command prints status informations about the SwarmRob daemon.

Parameters:
   - -i	[--interface] : Interface the command uses to communicate with the daemon *(optional)*

Example:
   >>> swarmrob daemon status -i lo

**swamrob daemon stop**
	The ``stop`` command stops the SwarmRob daemon.

Parameters:
   - -i	[--interface] : Interface the command uses to communicate with the daemon *(optional)*

Example:
   >>> swarmrob daemon start -i lo

**swamrob daemon check**
	The ``check`` command checks if docker is running successfully.

Parameters: *(None)*

Example:
   >>> swarmrob daemon check

