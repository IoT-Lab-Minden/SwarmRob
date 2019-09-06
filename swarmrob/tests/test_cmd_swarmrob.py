#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
from unittest.mock import patch
from swarmrob import master

from swarmrob.utils import pyro_interface


class TestCmdSwarmrob(TestCase):
    pass


def reset_daemon_dummy():
    swarmrob_daemon_proxy = pyro_interface.get_daemon_proxy("127.0.0.1")
    swarmrob_daemon_proxy.reset_dummy()
