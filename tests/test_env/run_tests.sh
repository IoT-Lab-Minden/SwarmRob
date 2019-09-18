RED='\033[0;31m'
GREEN='\033[0;32m'
interface='eth0'
docker-compose exec master /bin/bash -c "yes | swarmrob check" && echo "\n Result \n ========== \n ${GREEN}(Master) -> SwarmRob check passed" || echo "\n Result \n ========== \n ${RED}(Master) -> SwarmRob check failed"
output=$(docker-compose exec master /bin/bash -c "swarmrob daemon start -i $interface" | tr -d '\r') && echo "\n Result \n ========== \n ${GREEN}(Master) -> SwarmRob daemon start passed" || echo "\n Result \n ========== \n ${RED}(Master) -> SwarmRob daemon start failed"
echo "\n $output"
sleep 5s
output=$(docker-compose exec master /bin/bash -c "swarmrob master init -i $interface" | tr -d '\r') && echo "\n Result \n ========== \n ${GREEN}(Master) -> SwarmRob master init passed" || echo "\n Result \n ========== \n ${RED}(Master) -> SwarmRob master init failed"
echo "\n $output"
sleep 5s
out="$(tail -n1 <<<"$output")"
uuid="$(cut -d' ' -f1 <<<"$(cut -d'@' -f1 <<<"$out" | rev)" | rev)"
ip="$(cut -d' ' -f1 <<<"$(cut -d'@' -f2 <<<"$out")" | rev | cut -c 2- | rev)"
echo "UUID: $uuid@$ip"
echo "=============================== Begin check for Ubuntu 18.04 worker ================================ \n"
#ubuntu_18_04
docker-compose exec worker_ubuntu_18_04 /bin/bash -c "yes | swarmrob-worker check" && echo "\n Result \n ========== \n ${GREEN}(Ubuntu 18.04 Worker) -> SwarmRob check passed" || echo "\n Result \n ========== \n ${RED}(Ubuntu 18.04 Worker) -> SwarmRob check failed"
sleep 5s
docker-compose exec worker_ubuntu_18_04 /bin/bash -c "swarmrob-worker daemon start -i $interface" && echo "\n Result \n ========== \n ${GREEN}(Ubuntu 18.04 Worker) -> SwarmRob daemon start passed" || echo "\n Result \n ========== \n ${RED}(Ubuntu 18.04 Worker) -> SwarmRob daemon start failed"
sleep 5s
output=$(docker-compose exec worker_ubuntu_18_04 /bin/bash -c "swarmrob-worker worker join --uuid $uuid@$ip -i $interface") && echo "\n Result \n ========== \n ${GREEN}(Ubuntu 18.04 Worker) -> SwarmRob worker join passed" || echo "\n Result \n ========== \n ${RED}(Ubuntu 18.04 Worker) -> SwarmRob worker join failed"
sleep 5s
echo "\n $output"
echo "=============================== End check for Ubuntu 18.04 worker ================================ \n"
output=$(docker-compose exec master /bin/bash -c "swarmrob master swarm_status -i $interface" | tr -d '\r') && echo "\n Result \n ========== \n ${GREEN}(Master) -> SwarmRob master swarm_status with uuid:$uuid passed" || echo "\n Result \n ========== \n ${RED}(Master) -> SwarmRob master swarm_status with uuid:$uuid failed"
echo "\n $output"
sleep 5s
output=$(docker-compose exec master /bin/bash -c "swarmrob master start_swarm -u $uuid --compose_file /root/test_compose.yaml -i $interface" | tr -d '\r') && echo "\n Result \n ========== \n ${GREEN}(Master) -> SwarmRob master swarm_status with uuid:$uuid passed" || echo "\n Result \n ========== \n ${RED}(Master) -> SwarmRob master swarm_status with uuid:$uuid failed"
echo "\n $output"
sleep 5s
output=$(docker-compose exec master /bin/bash -c "swarmrob master swarm_status -i $interface" | tr -d '\r') && echo "\n Result \n ========== \n ${GREEN}(Master) -> SwarmRob master swarm_status with uuid:$uuid passed" || echo "\n Result \n ========== \n ${RED}(Master) -> SwarmRob master swarm_status with uuid:$uuid failed"
echo "\n $output"
sleep 5s
