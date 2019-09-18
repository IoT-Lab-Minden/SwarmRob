#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2018,2019 Aljoscha Pörtner
# Copyright 2019 André Kirsch
# This file is part of SwarmRob.
#
# SwarmRob is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SwarmRob is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SwarmRob.  If not, see <https://www.gnu.org/licenses/>.

import os
import sys
import traceback

import docker
import docker.errors

from logger import local_logger
from utils.errors import DockerException

MAX_RELOAD_TRIALS = 3


class SingletonType(type):
    """
    Helper class for singleton
    """
    def __call__(cls, *args, **kwargs):
        try:
            return cls.__instance
        except AttributeError:
            cls.__instance = super(SingletonType, cls).__call__(*args, **kwargs)
            return cls.__instance


class DockerInterface(object, metaclass=SingletonType):

    def __init__(self):
        """
            Initializing the docker interface
        :param self: Reference
        :return:
        """
        llogger = local_logger.LocalLogger()
        llogger.log_method_call(self.__class__.__name__, sys._getframe().f_code.co_name)
        self._docker_env = docker.from_env()
        self._docker_process = None

    def check_volumes(self, service_definition):
        """
            Check if volumes are available on the host system
        :param self: Reference
        :param service_definition: Definition of the service that was extracted out of the EDF
        :return: Returns a binary vector with size == number of services
        """
        llogger = local_logger.LocalLogger()
        llogger.log_method_call(self.__class__.__name__, sys._getframe().f_code.co_name)
        volumes = service_definition._volumes
        volume_vector = list()
        for volume_source, _ in list(volumes.items()):
            llogger.debug("Check volume source: %s", str(volume_source))
            if os.path.isdir(str(volume_source)) is True:
                volume_vector.append(1)
            else:
                volume_vector.append(0)
        return volume_vector

    def check_devices(self, service_definition):
        """
            Check if devices are available on the host system
        :param self: Reference
        :param service_definition: Definition of the service that was extracted out of the EDF
        :return: Returns a binary vector with size == number of services
        """
        llogger = local_logger.LocalLogger()
        llogger.log_method_call(self.__class__.__name__, sys._getframe().f_code.co_name)
        devices = service_definition._devices
        device_vector = list()
        for device in devices:
            device_source = device.split(":")[0]
            llogger.debug("Check device source: %s", str(device_source))
            if os.path.isdir(str(device_source)) is True:
                device_vector.append(1)
            else:
                device_vector.append(0)
        return device_vector

    def run_container_in_background(self, service_definition, remote_logger, swarm_uuid, worker_uuid, hostname=None,
                                    network=None):
        """
            Run the specified container as a daemon on the host system
        :param self: Reference
        :param service_definition: Definition of the service that was extracted out of the EDF
        :param remote_logger: Object of the remote logger
        :param swarm_uuid: UUID of the related SwarmRob swarm
        :param worker_uuid: UUID of the worker
        :param hostname: Hostname of the worker
        :param network: Network of the container
        :return:  Returns a docker result code
        """
        llogger = local_logger.LocalLogger()
        llogger.log_method_call(self.__class__.__name__, sys._getframe().f_code.co_name)
        if hostname is None:
            hostname = service_definition._id
        remote_logger.debug("Try to start %s", service_definition._tag)
        image_available = self._pull_image(service_definition._tag)
        if image_available:
            return self._start_container(service_definition, remote_logger, swarm_uuid, worker_uuid, hostname,
                                         network)
        else:
            llogger.debug("Unable to get image %s and start container", service_definition._tag)

    def _pull_image(self, image_tag):
        llogger = local_logger.LocalLogger()
        llogger.log_method_call(self.__class__.__name__, sys._getframe().f_code.co_name)
        if self.is_image_available(image_tag):
            llogger.debug('Image {0} already downloaded. Using downloaded image.'.format(image_tag))
            return True
        try:
            result = self._docker_env.images.pull(str(image_tag))
            return result is not None
        except docker.errors.APIError:
            llogger.debug("Unable to load image %s", image_tag)
            raise DockerException("Unable to load image " + image_tag)

    def _start_container(self, service_definition, remote_logger, swarm_uuid, worker_uuid, hostname, network):
        llogger = local_logger.LocalLogger()
        llogger.log_method_call(self.__class__.__name__, sys._getframe().f_code.co_name)
        try:
            result = self._docker_env.containers.create(str(service_definition._tag),
                                                        detach=True,
                                                        environment=service_definition._environment,
                                                        volumes=service_definition._volumes,
                                                        devices=service_definition._devices,
                                                        hostname=hostname,
                                                        network=network
                                                        )
            llogger.debug(result)
            remote_logger.debug(result)
            result.start()
            llogger.debug("\n" + service_definition.format_service_definition_as_table())
            remote_logger.debug("\n" + service_definition.format_service_definition_as_table())
            return result
        except (docker.errors.ImageNotFound, docker.errors.APIError):
            llogger.exception(traceback.format_exc())
            raise DockerException("Unable to create container for service " + service_definition._tag)

    def create_network(self, network_name="Default", network_driver="overlay"):
        """
            Create overlay network for the virtual connection between services in a swarm
        :param self: Reference
        :param network_name: Name of the overlay network (Default: "Default")
        :param network_driver: Driver of the network engine (Default: "overlay")
        :return: The created network or a docker result code
        """
        llogger = local_logger.LocalLogger()
        llogger.log_method_call(self.__class__.__name__, sys._getframe().f_code.co_name)
        try:
            if self.has_network_with_name(network_name) is False:
                llogger.debug("No network with name %s available. Try to create network. ", network_name)
                network = self._docker_env.networks.create(network_name, network_driver, attachable=True)
            else:
                network = self.get_network_by_name(network_name)
            return network
        except docker.errors.APIError:
            llogger.exception(traceback.format_exc())
            raise DockerException("Unable to create network " + network_name)

    def init_docker_swarm(self, interface):
        llogger = local_logger.LocalLogger()
        llogger.log_method_call(self.__class__.__name__, sys._getframe().f_code.co_name)
        try:
            self._docker_env.swarm.init(interface, force_new_cluster=True)
        except (docker.errors.APIError, ConnectionError):
            llogger.exception(traceback.format_exc())
            raise DockerException("Unable to init docker swarm")

    def join_docker_swarm(self, master_address, interface, join_token):
        llogger = local_logger.LocalLogger()
        llogger.log_method_call(self.__class__.__name__, sys._getframe().f_code.co_name)
        try:
            success = self._docker_env.swarm.join(remote_addrs=[master_address], join_token=join_token,
                                                  advertise_addr=interface)
            if not success:
                raise DockerException("Unable to join docker swarm with token " + join_token)
        except docker.errors.APIError:
            raise DockerException

    def get_join_token(self):
        llogger = local_logger.LocalLogger()
        llogger.log_method_call(self.__class__.__name__, sys._getframe().f_code.co_name)
        try:
            self._docker_env.swarm.reload()
            return self._docker_env.swarm.attrs['JoinTokens']['Worker']
        except (KeyError, docker.errors.APIError):
            llogger.debug('No Join Token available')
            llogger.exception(traceback.format_exc())
            raise DockerException("Unable to get join token")

    def has_network_with_name(self, network_name):
        """
            Check the existence of an overlay network by its name
        :param self: Reference
        :param network_name: Name of the network
        :return: Boolean if the network exists
        """
        llogger = local_logger.LocalLogger()
        llogger.log_method_call(self.__class__.__name__, sys._getframe().f_code.co_name)
        try:
            return len(self._docker_env.networks.list(names=[str(network_name)])) > 0
        except docker.errors.APIError:
            raise DockerException("Unable to get network list")

    def get_network_by_name(self, network_name):
        """
            Returns an overlay network by its name
        :param self: Reference
        :param network_name: Name of the network
        :return: Object of the network
        """
        llogger = local_logger.LocalLogger()
        llogger.log_method_call(self.__class__.__name__, sys._getframe().f_code.co_name)
        try:
            network_list = self._docker_env.networks.list(names=[str(network_name)])
            if len(network_list) == 0:
                raise DockerException("There is no network with name " + network_name)
            return network_list[0]
        except docker.errors.APIError:
            raise DockerException("Unable to get network list")

    def is_image_available(self, image_tag):
        """
            Checks if the docker image is downloaded or not
        :param image_tag: name of the image
        :return: True, when the image is available
        """
        llogger = local_logger.LocalLogger()
        llogger.log_method_call(self.__class__.__name__, sys._getframe().f_code.co_name)
        try:
            for image in self._docker_env.images.list():
                if len(image.tags) > 0 and (image.tags[0] == image_tag or image.tags[0].split(':', 1)[0] == image_tag):
                    return True
        except docker.errors.APIError:
            llogger.exception(traceback.format_exc())
            raise DockerException("Unable to get image list")
        return False

    def get_image_size(self, image_tag):
        """
            Returns the image size of the image
        :param image_tag: name of the image
        :return: size of image, if an error occurred or the image was not found -1 is returned instead
        """
        llogger = local_logger.LocalLogger()
        llogger.log_method_call(self.__class__.__name__, sys._getframe().f_code.co_name)
        if not self.is_image_available(image_tag):
            return -1
        try:
            image = self._docker_env.images.get(image_tag)
            if image is not None:
                return image.attrs.get('Size')
        except docker.errors.ImageNotFound:
            return -1
        except docker.errors.APIError:
            raise DockerException("Unable to get image")
