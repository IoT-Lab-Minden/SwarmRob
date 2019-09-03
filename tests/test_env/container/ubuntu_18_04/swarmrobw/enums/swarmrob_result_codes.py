#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum

class SwarmEngineResultCodes(Enum):
    '''
    ENUM Class for the SwarmRob result codes
    '''
    COMPOSITION_IS_READY = 1
    NOT_ENOUGH_WORKER = 2
    SWARM_STARTED = 3
    STARTING_SERVICE_ERROR = 4
    SWARM_NOT_INITIALIZED = 5
