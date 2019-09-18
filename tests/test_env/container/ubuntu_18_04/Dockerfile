FROM ubuntu:18.04
RUN apt-get update -yy && apt-get install -yy python3 python3-pip apt-transport-https ca-certificates curl gnupg-agent software-properties-common && pip3 install pip --upgrade
RUN apt-get remove -yy docker docker-engine docker.io containerd runc
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
RUN apt-key fingerprint 0EBFCD88
RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
RUN apt-get update && apt-get install -yy docker-ce docker-ce-cli containerd.io

COPY entrypoint.sh /root/entrypoint.sh
COPY swarmrobw /root/swarmrobw
COPY swarmrob /root/swarmrob
COPY test_compose.yaml /root/test_compose.yaml
COPY test_container /root/test_container
RUN chmod a+x /root/entrypoint.sh
ENTRYPOINT ["/bin/bash","-c","/root/entrypoint.sh"]
