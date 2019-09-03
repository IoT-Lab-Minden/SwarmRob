#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum

class DockerResultCodes(Enum):
    '''
    ENUM Class for the Docker Result Codes
    '''
    CONTAINER_CREATED = 0
    ERROR_IN_CONTAINER_CREATION = 1
    ERROR_IN_NETWORK_CREATION = 2
