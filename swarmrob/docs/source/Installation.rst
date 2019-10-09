.. _installation:

Installation 
================
Installing SwarmRob on a machine is an easy process. You just have to make sure that your machine is running one of the supported Linux distributions listed below and follow the steps to install SwarmRob.

Supported Linux distributions
-------------------------------
SwarmRob supports different Linux distributions as a Master node and as a Worker node. The toolkit was tested on the following distributions:

 * Ubuntu 18.04 Bionic
 * Ubuntu 16.04 Xenial
 * Debian 9 Stretch
 * Raspbian 9 Stretch (Worker node only)
 * Fedora 29

Installation Steps
--------------------
Before you can install SwarmRob for the first time, you need to install some necessary software. For simplicity we use the apt package manager. If you want to install SwarmRob on Fedora 29 you have to replace ``apt-get`` with ``dnf`` and you can skip the first step.

 1. Update the ``apt`` package index.

   ``sudo apt-get update``

 2. Install the following packages.

   ``sudo apt-get install python-dev python-tk python-pip``

 3. Make sure that your using the newest version of pip. You can check your version with the following command:

   ``pip --version``

   If you don't have the latest version or you are unsure, execute the following command.

   ``sudo pip install --upgrade pip``

 4. Install Docker CE. You can find an installation guide on the following website:
  
    https://docs.docker.com/install/

 5. Clone the SwarmRob GitHub Repository.

   ``git clone https://github.com/IoT-Lab-Minden/SwarmRob.git``

 6. Now you have two install options of SwarmRob you can choose from. The full version let's you use the device as a master and as a worker. The worker version only let's you use the device as a worker. (If you want to follow the GettingStarted tutorial, you will need at least one full version.)

    6.1. The full version requires a x64-based system. Install the full version with the following command:

      ``sudo pip install ./Swarmbot/swarmrob -r ./Swarmbot/swarmrob/requirements.txt``

    6.2. Install the worker version with the following command:

      ``sudo pip install ./Swarmbot/swarmrobw -r ./Swarmbot/swarmrobw/requirements.txt``

 7. To finish the installation SwarmRob needs to install some missing dependencies. To do this execute the following command.

      ``sudo swarmrob check``

 8. Now SwarmRob is ready to be used. You can learn how to use SwarmRob :ref:`here <gettingstarted>`.

