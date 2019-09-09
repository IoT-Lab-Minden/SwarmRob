import queue
import jsonpickle
from unittest import TestCase
from swarmrob.service_allocation import cost_calculation
from swarmrob.services import service
from swarmrob.logger import evaluation_logger


class WorkerDummy:
    def __init__(self, tag="", val=100):
        self.val = val
        self.tag = tag
        self.hostname = "foo"
        self.uuid = "bar"
        self.advertise_address = "127.0.0.1"

    def get_cpu_usage(self):
        return self.val

    def get_vram_usage(self):
        return self.val

    def get_swap_ram_usage(self):
        return self.val

    def get_remaining_image_download_size(self, image_tag):
        if self.tag == image_tag:
            return self.val
        return 0

    def get_bandwidth(self, repository):
        if repository is None:
            return self.val
        return 0

    def check_hardware(self, srv):
        if self.tag == jsonpickle.decode(srv).tag:
            return 1
        return 0


class TestCostCalculationInit(TestCase):
    def setUp(self):
        self.cost_calculation = default_setup()

    def test___init__(self):
        self.assertIsNotNone(self.cost_calculation.cpu_cost_weight)
        self.assertIsNotNone(self.cost_calculation.vram_cost_weight)
        self.assertIsNotNone(self.cost_calculation.swap_cost_weight)
        self.assertIsNotNone(self.cost_calculation.image_download_cost_weight)


class TestCostCalculationFunction(TestCase):
    def setUp(self):
        self.cost_calculation = default_setup()

    def test_cost_calculation(self):
        srv = service.Service("foo", "bar")
        worker = WorkerDummy("bar")
        q = queue.Queue()
        self.cost_calculation.calculate_costs_and_check_hardware_in_thread(0, srv, worker, q)
        self.assertEqual({0: {'cost': 99999, 'hw': 1}}, q.get())

    def test_cost_calculation_params_none(self):
        self.assertIsNone(self.cost_calculation.calculate_costs_and_check_hardware_in_thread(None, None, None, None))

    def test_cost_calculation_2(self):
        srv = service.Service("foo", "bar")
        worker = WorkerDummy("bar", 0)
        q = queue.Queue()
        self.cost_calculation.calculate_costs_and_check_hardware_in_thread(0, srv, worker, q)
        self.assertEqual({0: {'cost': 25000, 'hw': 1}}, q.get())

    def test_cost_calculation_3(self):
        srv = service.Service("foo", "foo:bar")
        worker = WorkerDummy("", 100)
        q = queue.Queue()
        self.cost_calculation.calculate_costs_and_check_hardware_in_thread(0, srv, worker, q)
        self.assertEqual({0: {'cost': 100000, 'hw': 0}}, q.get())

    def test_cost_calculation_4(self):
        srv = service.Service("foo", "foo:bar")
        worker = WorkerDummy("foo:bar", 50)
        q = queue.Queue()
        self.cost_calculation.calculate_costs_and_check_hardware_in_thread(0, srv, worker, q)
        self.assertEqual({0: {'cost': 40625, 'hw': 1}}, q.get())

    def test_cost_calculation_5(self):
        srv = service.Service("foo", "foo:bar")
        worker = WorkerDummy("foo:baz", 50)
        q = queue.Queue()
        self.cost_calculation.calculate_costs_and_check_hardware_in_thread(0, srv, worker, q)
        self.assertEqual({0: {'cost': 40625, 'hw': 0}}, q.get())


def default_setup():
    evaluation_logger.EvaluationLogger().enable(False)
    return cost_calculation.CostCalculation()
