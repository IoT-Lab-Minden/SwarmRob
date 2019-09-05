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

import sys

import jsonpickle

from ..logger import local_logger
from .default_cost_function import DefaultCostFunction


class CostCalculation:
    """
    Wrapper class for the cost calculation
    """

    def calculate_costs_and_check_hardware_in_thread(self, column_id, service,
                                                     worker, queue):
        """
            Wrapper method for the cost function
        :param column_id: ID of the cost matrix column
        :param service: Related service object
        :param worker: Related worker object
        :param queue: Thread result queue
        :return:
        """
        llogger = local_logger.LocalLogger()
        llogger.log_method_call(self.__class__.__name__, sys._getframe().f_code.co_name)
        llogger.debug("%s@%s", worker.uuid, worker.advertise_address)
        cost_and_hardware_column = dict()
        hardware_row_for_service = worker.check_hardware(jsonpickle.encode(service))
        cost_row_for_service = DefaultCostFunction().calculate_costs(worker, service)
        cost_and_hardware_column.update({"cost": cost_row_for_service})
        cost_and_hardware_column.update({"hw": hardware_row_for_service})
        thread_return = dict()
        thread_return.update({column_id: cost_and_hardware_column})
        llogger.debug(thread_return)
        queue.put(thread_return)
