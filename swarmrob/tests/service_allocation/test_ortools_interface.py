from unittest import TestCase
from swarmrob.swarmengine.swarm_engine_worker import Worker
from swarmrob.service_allocation import ortools_interface


class TestOrToolsInterfaceAllocateServicesToWorkers(TestCase):
    def test_default_parameters(self):
        result = ortools_interface.allocate_services_to_workers()
        self.assertIsNone(result)

    def test_one_worker_zero_services(self):
        workers = {"worker_1": Worker("foo", "lo")}
        result = ortools_interface.allocate_services_to_workers(workers=workers)
        self.assertIsNone(result)

    def test_multiple_workers_zero_services(self):
        workers = {"worker_1": Worker("foo", "lo"), "worker_2": Worker("foo", "lo")}
        result = ortools_interface.allocate_services_to_workers(workers=workers)
        self.assertIsNone(result)

    def test_zero_workers_one_service(self):
        result = ortools_interface.allocate_services_to_workers(services=["service_1"])
        self.assertIsNone(result)

    def test_zero_workers_multiple_services(self):
        result = ortools_interface.allocate_services_to_workers(services=["service_1", "service_2"])
        self.assertIsNone(result)

    def test_one_worker_one_service(self):
        worker_1 = Worker("foo", "lo")
        workers = {"worker_1": worker_1}
        result = ortools_interface.allocate_services_to_workers(workers=workers, services=["service_1"])
        self.assertEqual({worker_1: ["service_1"]}, result)

    def test_one_worker_multiple_services(self):
        worker_1 = Worker("foo", "lo")
        workers = {"worker_1": worker_1}
        result = ortools_interface.allocate_services_to_workers(workers=workers, services=["service_1", "service_2"])
        self.assertEqual({worker_1: ["service_1", "service_2"]}, result)

    def test_multiple_worker_no_matrices(self):
        worker_1 = Worker("foo", "lo")
        worker_2 = Worker("foo", "lo")
        workers = {"worker_1": worker_1, "worker_2": worker_2}
        result = ortools_interface.allocate_services_to_workers(workers=workers, services=["service_1"])
        self.assertIsNone(result)

    def test_multiple_worker_empty_matrices(self):
        worker_1 = Worker("foo", "lo")
        worker_2 = Worker("foo", "lo")
        workers = {"worker_1": worker_1, "worker_2": worker_2}
        result = ortools_interface.allocate_services_to_workers(workers=workers, services=["service_1"],
                                                                hardware_matrix=[], cost_matrix=[], capacity_matrix=[])
        self.assertIsNone(result)

    def test_mismatched_matrices(self):
        worker_1 = Worker("foo", "lo")
        worker_2 = Worker("foo", "lo")
        workers = {"worker_1": worker_1, "worker_2": worker_2}
        result = ortools_interface.allocate_services_to_workers(workers=workers, services=["service_1", "service_2"],
                                                                hardware_matrix=[[1], [1, 1]],
                                                                cost_matrix=[[4]],
                                                                capacity_matrix=[[1], [1]])
        self.assertIsNone(result)

    def test_autogenerated_dependency_matrix(self):
        worker_1 = Worker("foo", "lo")
        worker_2 = Worker("foo", "lo")
        workers = {"worker_1": worker_1, "worker_2": worker_2}
        result = ortools_interface.allocate_services_to_workers(workers=workers, services=["service_1", "service_2"],
                                                                hardware_matrix=[[1, 1], [1, 1]],
                                                                cost_matrix=[[4, 3], [4, 3]])
        self.assertTrue((result[worker_1] == ["service_1"] and result[worker_2] == ["service_2"]) or (result[worker_1]
                        == ["service_2"] and result[worker_2] == ["service_1"]))

    def test_filled_matrices(self):
        worker_1 = Worker("foo", "lo")
        worker_2 = Worker("foo", "lo")
        workers = {"worker_1": worker_1, "worker_2": worker_2}
        result = ortools_interface.allocate_services_to_workers(workers=workers, services=["service_1", "service_2"],
                                                                hardware_matrix=[[1, 1], [1, 1]],
                                                                cost_matrix=[[4, 3], [4, 3]],
                                                                capacity_matrix=[[1, 1], [1, 1]])
        self.assertTrue((result[worker_1] == ["service_1"] and result[worker_2] == ["service_2"]) or (result[worker_1]
                        == ["service_2"] and result[worker_2] == ["service_1"]))
