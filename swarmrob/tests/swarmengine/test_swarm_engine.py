import os

from unittest import TestCase
from unittest.mock import patch

from daemon_dummy import worker_dummy
from swarmrob.services import edf_parser
from swarmrob.swarmengine import swarm_engine, swarm_engine_master, swarm_engine_worker
from swarmrob.utils.errors import DockerException, SwarmException

DIR = os.path.dirname(__file__)
COMPOSITION_FILE = DIR + "/compose_test.yaml"


class DockerInterfaceDummy:
    def __init__(self):
        pass

    def init_docker_swarm(self, interface):
        if not interface:
            raise DockerException

    def create_network(self, network_name):
        if not network_name:
            raise DockerException


class TestSwarmEngineInit(TestCase):
    def setUp(self):
        self.swarm_engine = default_setup()

    def test_init(self):
        self.assertIsNone(self.swarm_engine.swarm)


@patch('swarmrob.dockerengine.docker_interface.DockerInterface', DockerInterfaceDummy)
class TestSwarmEngineCreateNewSwarm(TestCase):
    def setUp(self):
        self.swarm_engine = default_setup()

    def test_create_new_swarm(self):
        master = swarm_engine_master.Master("lo", "127.0.0.1")
        self.assertIsNotNone(self.swarm_engine.create_new_swarm(master, "foo"))
        self.assertIsNotNone(self.swarm_engine.swarm)

    def test_create_new_swarm_swarm_uuid_none(self):
        master = swarm_engine_master.Master("lo", "127.0.0.1")
        self.assertIsNotNone(self.swarm_engine.create_new_swarm(master, None))
        self.assertIsNotNone(self.swarm_engine.swarm)

    def test_create_new_swarm_master_none(self):
        self.assertIsNone(self.swarm_engine.create_new_swarm(None, "foo"))
        self.assertIsNone(self.swarm_engine.swarm)


def worker_join_docker_swarm_dummy(self, advertise_address, join_token):
    if not advertise_address or not join_token:
        raise RuntimeError


@patch('swarmrob.dockerengine.docker_interface.DockerInterface', DockerInterfaceDummy)
@patch('swarmrob.swarmengine.swarm_engine_worker.Worker.join_docker_swarm', worker_join_docker_swarm_dummy)
class TestSwarmEngineRegisterWorkerInSwarm(TestCase):
    def setUp(self):
        self.swarm_engine = default_setup()
        self.master = swarm_engine_master.Master("lo", "127.0.0.1")
        self.swarm_engine.create_new_swarm(self.master, "foo")

    def test_register_worker_in_swarm(self):
        worker = swarm_engine_worker.Worker("foo", "lo", "bar")
        self.swarm_engine.register_worker_in_swarm("foo", worker)
        self.assertEqual({'bar': worker}, self.swarm_engine.swarm._worker_list)

    def test_register_worker_in_swarm_swarm_uuid_none(self):
        worker = swarm_engine_worker.Worker("foo", "lo", "bar")
        self.swarm_engine.register_worker_in_swarm(None, worker)
        self.assertEqual({}, self.swarm_engine.swarm._worker_list)

    def test_register_worker_in_swarm_worker_none(self):
        self.swarm_engine.register_worker_in_swarm("foo", None)
        self.assertEqual({}, self.swarm_engine.swarm._worker_list)


class TestSwarmEngineUnregisterWorkerInSwarm(TestCase):
    def setUp(self):
        self.swarm_engine = default_setup()
        self.master = swarm_engine_master.Master("lo", "127.0.0.1")
        self.swarm_engine.create_new_swarm(self.master, "foo")

    def test_unregister_worker_in_swarm(self):
        worker = swarm_engine_worker.Worker("foo", "lo", "bar")
        self.swarm_engine.register_worker_in_swarm("foo", worker)
        self.swarm_engine.unregister_worker_in_swarm("foo", "bar")
        self.assertEqual({}, self.swarm_engine.swarm._worker_list)

    def test_unregister_worker_in_swarm_swarm_uuid_none(self):
        worker = swarm_engine_worker.Worker("foo", "lo", "bar")
        self.swarm_engine.register_worker_in_swarm("foo", worker)
        self.swarm_engine.unregister_worker_in_swarm(None, "bar")
        self.assertEqual({'bar': worker}, self.swarm_engine.swarm._worker_list)

    def test_unregister_worker_in_swarm_worker_uuid_none(self):
        worker = swarm_engine_worker.Worker("foo", "lo", "bar")
        self.swarm_engine.register_worker_in_swarm("foo", worker)
        self.swarm_engine.unregister_worker_in_swarm("foo", None)
        self.assertEqual({'bar': worker}, self.swarm_engine.swarm._worker_list)


class TestSwarmEngineStartSwarmByComposition(TestCase):
    def setUp(self):
        self.swarm_engine = default_setup()
        self.composition = edf_parser.create_service_composition_from_edf(COMPOSITION_FILE)

    def test_start_swarm_by_composition(self):
        master = swarm_engine_master.Master("lo", "127.0.0.1")
        self.swarm_engine.create_new_swarm(master, "foo")
        self.swarm_engine.register_worker_in_swarm("foo", worker_dummy.Worker("foo", "lo", "bar"))
        self.assertTrue(self.swarm_engine.start_swarm_by_composition(self.composition, "foo"))

    def test_start_swarm_by_composition_no_workers(self):
        master = swarm_engine_master.Master("lo", "127.0.0.1")
        self.swarm_engine.create_new_swarm(master, "foo")
        self.assertFalse(self.swarm_engine.start_swarm_by_composition(self.composition, "foo"))

    def test_start_swarm_by_composition_swarm_not_initialized(self):
        try:
            self.swarm_engine.start_swarm_by_composition(self.composition, "foo")
            self.fail(msg="Not initialized swarms should throw a SwarmException")
        except SwarmException:
            pass

    def test_start_swarm_by_composition_composition_none(self):
        try:
            self.swarm_engine.start_swarm_by_composition(None, "foo")
            self.fail(msg="None composition should throw a SwarmException")
        except SwarmException:
            pass

    def test_start_swarm_by_composition_swarm_uuid_none(self):
        try:
            self.swarm_engine.start_swarm_by_composition(self.composition, None)
            self.fail(msg="None swarm_uuid should throw a SwarmException")
        except SwarmException:
            pass


def default_setup():
    engine = swarm_engine.SwarmEngine()
    engine.__init__()
    return engine
