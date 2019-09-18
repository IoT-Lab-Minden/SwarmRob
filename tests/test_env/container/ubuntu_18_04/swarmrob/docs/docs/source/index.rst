.. SwarmRob-Full documentation master file, created by
   sphinx-quickstart on Tue Aug 29 17:36:22 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

SwarmRob for Python
=========================================
A python framework that uses container technologies and orchestration to enable the 
simple sharing of experimental artifacts and improve the reproducibility 
in robotics research.

Installation
-----------------------------------------
The latest stable version os available on PyPI. SwarmRob is separated into a full version and a worker version.
The full version is needed to run a swarm master and requires an x64-based system. It can be installed using::

	pip install swarmrob-full 

The worker version runs on every system architecture from ``ARM`` to ``x64`` and should be used on the worker nodes. It can be installed using::

	pip install swarmrob-worker

Getting started
-----------------------------------------
In order to setup the required infrastructure, the toolkit needs to be installed on every participating node but at least on one worker and one master.
A figure of the typical setup is shown in Figure todo.

TODO PICTURE

Step 1: *Prepare Container Definition Files (CDFs)*
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Step 2: *Prepare Experiment Definition Files (EDFs)*
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Step 3: *Setup a Master Node*
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. toctree::
   :maxdepth: 2

   Master
   Worker
   Daemon
   Changelog


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
