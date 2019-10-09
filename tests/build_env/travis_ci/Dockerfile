FROM ubuntu:16.04

RUN apt-get update && apt-get -y install curl python3 python3-pip wget python3-sphinx git software-properties-common apt-transport-https ca-certificates

RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
RUN apt-get update 
RUN apt-get -y install docker-ce docker-ce-cli containerd.io
WORKDIR "~"
RUN wget http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh -O miniconda.sh
RUN chmod +x miniconda.sh
RUN ./miniconda.sh -b
ENV PATH="/root/miniconda2/bin:${PATH}"
RUN echo $PATH
RUN conda update --yes conda
RUN git clone https://AljoschaP:3609264702e5d92175dcee58e8c841c0646c0859@github.com/AljoschaP/SwarmRob.git
ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8'
RUN apt-get install -y locales && locale-gen en_US.UTF-8 
RUN pip3 install --upgrade setuptools pip
RUN cd SwarmRob && pip3 install $PWD/swarmrob -r $PWD/swarmrob/requirements.txt && pip3 install $PWD/swarmrob/tests/dummy_daemon -r $PWD/swarmrob/tests/dummy_daemon/requirements.txt
RUN pip3 install -U sphinx
RUN pip3 install --user travis-sphinx
COPY run.sh /root/run.sh
ENTRYPOINT ["/root/run.sh"]
