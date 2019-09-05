from unittest import TestCase
from logger import remote_logger


class TestRemoteLogger(TestCase):
    def setUp(self):
        self.logger = remote_logger.RemoteLogger("127.0.0.1", "0", "foo", "bar")
        self.broken_logger = remote_logger.RemoteLogger(None, None, None, None)

    def test_init_logger(self):
        self.assertIsNotNone(self.logger.swarm_uuid)
        self.assertIsNotNone(self.logger.worker_uuid)
        self.assertIsNotNone(self.logger.remote_logger)

    def test_init_logger(self):
        self.assertIsNone(self.broken_logger.swarm_uuid)
        self.assertIsNone(self.broken_logger.worker_uuid)
        self.assertIsNone(self.broken_logger.remote_logger)

    def test_debug(self):
        self.assertTrue(self.logger.debug("DEBUG_MESSAGE"))

    def test_debug_disabled(self):
        self.assertFalse(self.broken_logger.debug("DEBUG_MESSAGE"))

    def test_error(self):
        self.assertTrue(self.logger.error("DEBUG_MESSAGE"))

    def test_error_disabled(self):
        self.assertFalse(self.broken_logger.error("DEBUG_MESSAGE"))

    def test_exception(self):
        self.assertTrue(self.logger.error(Exception("Exception"), "DEBUG_MESSAGE"))

    def test_exception_disabled(self):
        self.assertFalse(self.broken_logger.error(Exception("Exception"), "DEBUG_MESSAGE"))
