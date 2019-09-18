# This scripts tests SwarmRob locally on one computer.
# Param: EDF used to run the test.

# 1. Start the daemon
echo "1. Starting the SwarmRob daemon"
sudo swarmrob daemon start -v
sleep 5
# 2. Initialize the SwarmRob master
echo "2. Initializing the SwarmRob master"
sudo swarmrob master init -u foo
sleep 1
# 3. Let a worker join the swarm
echo "3. Worker joining the swarm"
sudo swarmrob worker join -u foo@$(hostname -I | cut -d' ' -f1)
sleep 1
# 4. Run an EDF.
if test -z "$1" 
then
	echo "4. No EDF given. Skipping EDF Test."
else
	echo "4. Running EDF test $1"
	sudo swarmrob master start_swarm -u foo -c $1
	sleep 1
fi
# 5. Kill the SwarmRob daemon
echo "5. Killing the SwarmRob daemon"
sudo pkill -f swarmrob
