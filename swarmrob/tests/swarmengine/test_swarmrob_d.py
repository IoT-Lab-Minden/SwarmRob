import jsonpickle
import time

from unittest import TestCase
from unittest.mock import patch

from swarmrob import master
from swarmrob.logger import evaluation_logger
from swarmrob.services import service_composition
from swarmrob.swarmengine import swarmrob_d, swarm_engine, swarm_engine_worker, mode
from swarmrob.utils import pyro_interface
from swarmrob.utils.errors import SwarmException


class TestSwarmrobDInit(TestCase):
    def setUp(self):
        self.daemon = default_setup()

    def test_init(self):
        self.assertEqual(True, self.daemon._daemon_running)
        self.assertEqual("lo", self.daemon._interface)
        self.assertIsNone(self.daemon._master)
        self.assertIsNotNone(self.daemon._pyro_daemon)
        self.assertEqual(swarm_engine.SwarmEngine(), self.daemon._swarm_engine)
        self.assertEqual(dict(), self.daemon._swarm_list_of_worker)


# Not testing the methods _close_pyro_daemon, shutdown, _unregister_daemon_at_nameservice because they may cause
# problems with the swarmrob daemon dummy

class TestSwarmrobDIsDaemonRunning(TestCase):
    def setUp(self):
        self.daemon = default_setup()

    def test_is_daemon_running(self):
        self.assertTrue(self.daemon.is_daemon_running())

    def test_is_daemon_running_false(self):
        self.daemon._set_daemon_running(False)
        self.assertFalse(self.daemon.is_daemon_running())


class TestSwarmrobDSetDaemonRunning(TestCase):
    def setUp(self):
        self.daemon = default_setup()

    def test_set_daemon_running(self):
        self.daemon._set_daemon_running(True)
        self.assertTrue(self.daemon._daemon_running)

    def test_set_daemon_running_false(self):
        self.daemon._set_daemon_running(False)
        self.assertFalse(self.daemon._daemon_running)


# Not testing create_new_swarm and register_worker, unregister_worker because of conflicts with Pyro4


class TestSwarmrobDRegisterWorkerAtLocalDaemon(TestCase):
    def setUp(self):
        self.daemon = default_setup()

    def test_register_worker_at_local_daemon(self):
        worker = swarm_engine_worker.Worker("foo", "lo")
        self.daemon.register_worker_at_local_daemon(worker)
        self.assertEqual({"foo": worker}, self.daemon._swarm_list_of_worker)

    def test_register_worker_at_local_daemon_register_the_same_twice(self):
        worker = swarm_engine_worker.Worker("foo", "lo")
        self.daemon.register_worker_at_local_daemon(worker)
        self.daemon.register_worker_at_local_daemon(worker)
        self.assertEqual({"foo": worker}, self.daemon._swarm_list_of_worker)

    def test_register_worker_at_local_daemon_worker_none(self):
        self.daemon.register_worker_at_local_daemon(None)
        self.assertEqual({}, self.daemon._swarm_list_of_worker)


class TestSwarmrobDUnregisterWorkerAtLocalDaemon(TestCase):
    def setUp(self):
        self.daemon = default_setup()

    def test_unregister_worker_at_local_daemon(self):
        worker = swarm_engine_worker.Worker("foo", "lo")
        self.daemon.register_worker_at_local_daemon(worker)
        self.daemon.unregister_worker_at_local_daemon("foo")
        self.assertEqual({}, self.daemon._swarm_list_of_worker)

    def test_unregister_worker_at_local_daemon_worker_uuid_none(self):
        worker = swarm_engine_worker.Worker("foo", "lo")
        self.daemon.register_worker_at_local_daemon(worker)
        self.daemon.unregister_worker_at_local_daemon(None)
        self.assertEqual({"foo": worker}, self.daemon._swarm_list_of_worker)

    def test_unregister_worker_at_local_daemon_no_worker_registered(self):
        self.daemon.unregister_worker_at_local_daemon("foo")
        self.assertEqual({}, self.daemon._swarm_list_of_worker)


def worker_join_docker_swarm_dummy(self, master_address, join_token):
    if master_address is None or join_token is None:
        raise RuntimeError


@patch('swarmrob.swarmengine.swarm_engine_worker.Worker.join_docker_swarm', worker_join_docker_swarm_dummy)
class TestSwarmrobDJoinDockerSwarm(TestCase):
    def setUp(self):
        self.daemon = default_setup()

    def test_join_docker_swarm(self):
        worker = swarm_engine_worker.Worker("foo", "lo")
        self.daemon.register_worker_at_local_daemon(worker)
        self.assertTrue(self.daemon.join_docker_swarm("foo", "127.0.0.1", "bar"))

    def test_join_docker_swarm_worker_not_registered(self):
        self.assertFalse(self.daemon.join_docker_swarm("foo", "127.0.0.1", "bar"))

    def test_join_docker_swarm_catching_runtime_exception(self):
        worker = swarm_engine_worker.Worker("foo", "lo")
        self.daemon.register_worker_at_local_daemon(worker)
        self.assertFalse(self.daemon.join_docker_swarm("foo", None, None))


class TestSwarmrobDGetMode(TestCase):
    def setUp(self):
        self.daemon = default_setup()

    def test_not_defined(self):
        self.assertEqual(mode.Mode.NOT_DEFINED, jsonpickle.decode(self.daemon.get_mode()))

    def test_worker(self):
        worker = swarm_engine_worker.Worker("foo", "lo")
        self.daemon.register_worker_at_local_daemon(worker)
        self.assertEqual(mode.Mode.WORKER, jsonpickle.decode(self.daemon.get_mode()))

    def test_master(self):
        self.daemon._master = {}
        self.assertEqual(mode.Mode.MASTER, jsonpickle.decode(self.daemon.get_mode()))


class TestSwarmrobDGetWorkerStatusAsJson(TestCase):
    def setUp(self):
        self.daemon = default_setup()

    def test_get_worker_status_as_json(self):
        worker = swarm_engine_worker.Worker("foo", "lo")
        self.daemon.register_worker_at_local_daemon(worker)
        self.assertEqual(1, len(jsonpickle.decode(self.daemon.get_worker_status_as_json())))

    def test_get_worker_status_as_json_none_registered(self):
        self.assertEqual({}, jsonpickle.decode(self.daemon.get_worker_status_as_json()))


def swarm_engine_start_swarm_dummy(self, composition, swarm_uuid):
    if composition is None or swarm_uuid is None:
        raise SwarmException


@patch('swarmrob.swarmengine.swarm_engine.SwarmEngine.start_swarm_by_composition', swarm_engine_start_swarm_dummy)
class TestSwarmrobDStartSwarmByComposition(TestCase):
    def setUp(self):
        self.daemon = default_setup()

    def test_start_swarm_by_composition(self):
        composition = service_composition.ServiceComposition()
        self.daemon.start_swarm_by_composition(jsonpickle.encode(composition), "foo")

    def test_start_swarm_by_composition_composition_none(self):
        try:
            self.daemon.start_swarm_by_composition(None, "foo")
            self.fail()
        except RuntimeError:
            pass

    def test_start_swarm_by_composition_swarm_uuid_none(self):
        composition = service_composition.ServiceComposition()
        try:
            self.daemon.start_swarm_by_composition(jsonpickle.encode(composition), None)
            self.fail()
        except RuntimeError:
            pass

    def test_start_swarm_by_composition_composition_not_pickled(self):
        composition = service_composition.ServiceComposition()
        try:
            self.daemon.start_swarm_by_composition(composition, "foo")
            self.fail()
        except RuntimeError:
            pass


@patch('sys.argv', ['-i', 'lo'])
class TestSwarmrobDGetSwarmStatusAsJson(TestCase):
    def setUp(self):
        self.daemon = default_setup()
        reset_daemon_dummy()

    def test_get_swarm_status_as_json(self):
        master.init_swarm()
        self.assertIsNotNone(self.daemon.get_swarm_status_as_json())

    def test_get_swarm_status_as_json_master_not_initialized(self):
        self.assertIsNone(self.daemon.get_swarm_status_as_json())


class TestSwarmrobDConfigureEvaluationLogger(TestCase):
    def setUp(self):
        self.daemon = default_setup()
        self.eval_log = evaluation_logger.EvaluationLogger()

    def test_configure_evaluation_logger(self):
        self.daemon.configure_evaluation_logger("foo", "bar", True)
        self.assertEqual("foo", self.eval_log.log_folder)
        self.assertEqual("bar", self.eval_log.log_ident)
        self.assertTrue(self.eval_log.enabled)

    def test_configure_evaluation_logger_disabled(self):
        self.daemon.configure_evaluation_logger("foo", "bar", False)
        self.assertEqual("foo", self.eval_log.log_folder)
        self.assertEqual("bar", self.eval_log.log_ident)
        self.assertFalse(self.eval_log.enabled)

    def test_configure_evaluation_logger_None(self):
        self.daemon.configure_evaluation_logger("foo", "bar", True)
        self.daemon.configure_evaluation_logger(None, None, True)
        self.assertIsNotNone(self.eval_log.log_folder)
        self.assertIsNotNone(self.eval_log.log_ident)
        self.assertTrue(self.eval_log.enabled)

    def test_configure_evaluation_logger_None_and_disabled(self):
        self.daemon.configure_evaluation_logger("foo", "bar", True)
        self.daemon.configure_evaluation_logger(None, None, False)
        self.assertIsNotNone(self.eval_log.log_folder)
        self.assertIsNotNone(self.eval_log.log_ident)
        self.assertFalse(self.eval_log.enabled)


class TestSwarmrobDResetEvaluationLogger(TestCase):
    def setUp(self):
        self.daemon = default_setup()
        self.eval_log = evaluation_logger.EvaluationLogger()

    def test_reset_evaluation_logger(self):
        timer = self.eval_log.timestr
        time.sleep(1)
        self.daemon.reset_evaluation_logger()
        self.assertNotEqual(timer, self.eval_log.timestr)


def reset_daemon_dummy():
    swarmrob_daemon_proxy = pyro_interface.get_daemon_proxy("127.0.0.1")
    swarmrob_daemon_proxy.reset_dummy()


def default_setup():
    pyro_daemon = jsonpickle.decode(pyro_interface.get_daemon_proxy("127.0.0.1").get_pyro_daemon())
    daemon = swarmrob_d.SwarmRobDaemon("lo", pyro_daemon)
    daemon.__init__("lo", pyro_daemon)
    return daemon
