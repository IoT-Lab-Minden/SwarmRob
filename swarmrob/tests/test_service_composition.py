from unittest import TestCase
from swarmengine import swarm_engine_worker
from services import service_composition, service


class TestServiceComposition(TestCase):
    def setUp(self):
        self.service = service.Service()
        self.worker = swarm_engine_worker.Worker("foo", "lo")
        self.composition = service_composition.ServiceComposition()

    def test_empty_composition(self):
        self.assertTrue(self.composition.is_empty())
        self.assertEqual(0, self.composition.get_service_count())

    def test_add_service(self):
        self.composition.add_service("KEY", self.service)
        self.assertFalse(self.composition.is_empty())
        self.assertEqual(1, self.composition.get_service_count())
        self.assertEqual(self.service, self.composition.get_service("KEY"))

    def test_add_service_none_key(self):
        self.composition.add_service(None, self.service)
        self.assertTrue(self.composition.is_empty())

    def test_add_service_empty_key(self):
        self.composition.add_service("", self.service)
        self.assertTrue(self.composition.is_empty())

    def test_add_service_none_service(self):
        self.composition.add_service("KEY", None)
        self.assertTrue(self.composition.is_empty())

    def test_assign_worker_to_service(self):
        self.composition.add_service("KEY", self.service)
        self.composition.assign_worker_to_service("KEY", self.worker)
        self.assertEqual(self.worker.uuid, self.composition.get_worker_key("KEY"))

    def test_assign_worker_to_not_existing_service(self):
        self.composition.assign_worker_to_service("KEY", self.worker)
        self.assertEqual(None, self.composition.get_worker_key("KEY"))

    def test_assign_worker_to_none_service(self):
        self.composition.assign_worker_to_service(None, self.worker)
        self.assertEqual(None, self.composition.get_worker_key(None))

    def test_assign_worker_to_service_none_worker(self):
        self.composition.add_service("KEY", self.service)
        self.composition.assign_worker_to_service("KEY", None)
        self.assertEqual(None, self.composition.get_worker_key("KEY"))

    def test_assign_worker_to_services(self):
        self.composition.add_service("KEY", self.service)
        self.composition.add_service("KEY2", self.service)
        self.composition.assign_worker_to_services(["KEY", "KEY2"], self.worker)
        self.assertEqual(self.worker.uuid, self.composition.get_worker_key("KEY"))
        self.assertEqual(self.worker.uuid, self.composition.get_worker_key("KEY2"))

    def test_assign_worker_to_services_none_worker(self):
        self.composition.add_service("KEY", self.service)
        self.composition.add_service("KEY2", self.service)
        self.composition.assign_worker_to_services(["KEY", "KEY2"], None)
        self.assertEqual(None, self.composition.get_worker_key("KEY"))
        self.assertEqual(None, self.composition.get_worker_key("KEY2"))

    def test_assign_worker_to_services_none_list(self):
        self.composition.add_service("KEY", self.service)
        self.composition.add_service("KEY2", self.service)
        self.composition.assign_worker_to_services(None, self.worker)
        self.assertEqual(None, self.composition.get_worker_key("KEY"))
        self.assertEqual(None, self.composition.get_worker_key("KEY2"))

    def test_assign_worker_to_services_empty_list(self):
        self.composition.add_service("KEY", self.service)
        self.composition.add_service("KEY2", self.service)
        self.composition.assign_worker_to_services([], self.worker)
        self.assertEqual(None, self.composition.get_worker_key("KEY"))
        self.assertEqual(None, self.composition.get_worker_key("KEY2"))

    def test_get_open_allocations(self):
        self.composition.add_service("KEY", self.service)
        self.composition.add_service("KEY2", self.service)
        self.assertEqual(sorted(["KEY", "KEY2"]), sorted(self.composition.get_open_allocations()))

    def test_get_open_allocations_empty(self):
        self.assertEqual([], self.composition.get_open_allocations())

    def test_get_open_allocations_one_allocated(self):
        self.composition.add_service("KEY", self.service)
        self.composition.add_service("KEY2", self.service)
        self.composition.assign_worker_to_service("KEY", self.worker)
        self.assertEqual(sorted(["KEY2"]), sorted(self.composition.get_open_allocations()))

    def test_get_open_allocations_all_allocated(self):
        self.composition.add_service("KEY", self.service)
        self.composition.add_service("KEY2", self.service)
        self.composition.assign_worker_to_services(["KEY", "KEY2"], self.worker)
        self.assertEqual([], self.composition.get_open_allocations())

    def test_get_list_of_allocated_workers(self):
        self.composition.add_service("KEY", self.service)
        self.composition.add_service("KEY2", self.service)
        self.composition.assign_worker_to_services(["KEY", "KEY2"], self.worker)
        self.assertEqual([self.worker.uuid, self.worker.uuid], self.composition.get_list_of_allocated_workers())

    def test_get_list_of_allocated_workers_empty(self):
        self.assertEqual([], self.composition.get_list_of_allocated_workers())

    def test_get_list_of_allocated_workers_none_allocated(self):
        self.composition.add_service("KEY", self.service)
        self.composition.add_service("KEY2", self.service)
        self.assertEqual([], self.composition.get_list_of_allocated_workers())

    def test_get_worker_key(self):
        self.composition.add_service("KEY", self.service)
        self.composition.assign_worker_to_service("KEY", self.worker)
        self.assertEqual(self.worker.uuid, self.composition.get_worker_key("KEY"))

    def test_get_worker_key_none(self):
        self.composition.add_service("KEY", self.service)
        self.composition.assign_worker_to_service("KEY", self.worker)
        self.assertEqual(None, self.composition.get_worker_key(None))

    def test_get_service(self):
        self.composition.add_service("KEY", self.service)
        self.assertEqual(self.service, self.composition.get_service("KEY"))

    def test_get_service_none_key(self):
        self.composition.add_service("KEY", self.service)
        self.assertEqual(None, self.composition.get_service(None))

    def test_get_service_key_list(self):
        self.composition.add_service("KEY", self.service)
        self.composition.add_service("KEY2", self.service)
        self.assertEqual(["KEY", "KEY2"], self.composition.get_service_key_list())

    def test_get_service_key_list_empty(self):
        self.assertEqual([], self.composition.get_service_key_list())

    def test_get_service_key_list_allocated_worker(self):
        self.composition.add_service("KEY", self.service)
        self.composition.add_service("KEY2", self.service)
        self.composition.assign_worker_to_service("KEY", self.worker)
        self.assertEqual(["KEY", "KEY2"], self.composition.get_service_key_list())
