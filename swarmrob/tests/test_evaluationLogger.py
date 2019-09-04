import time
from unittest import TestCase
from os import path
from logger import evaluation_logger


class TestEvaluationLogger(TestCase):
    def setUp(self):
        self.logger = evaluation_logger.EvaluationLogger()
        self.logger.set_log_folder("log_folder")
        self.logger.set_log_ident("log_ident")
        self.logger.enable()
        self.logger.reset_time()

    def test_set_log_folder(self):
        self.logger.set_log_folder("new_log_folder")
        self.assertEqual("new_log_folder", self.logger.log_folder)
        self.assertTrue(self.logger.enabled)

    def test_set_log_ident(self):
        self.logger.set_log_ident("new_log_ident")
        self.assertEqual("new_log_ident", self.logger.log_ident)
        self.assertTrue(self.logger.enabled)

    def test_set_log_folder_none(self):
        self.logger.set_log_folder(None)
        self.assertEqual(None, self.logger.log_folder)
        self.assertFalse(self.logger.enabled)

    def test_set_log_ident_none(self):
        self.logger.set_log_ident(None)
        self.assertEqual(None, self.logger.log_ident)
        self.assertTrue(self.logger.enabled)

    def test_set_log_folder_user_path(self):
        self.logger.set_log_folder("~/new_log_folder")
        self.assertEqual(path.expanduser("~") + "/new_log_folder", self.logger.log_folder)
        self.assertTrue(self.logger.enabled)

    def test_set_log_folder_empty(self):
        self.logger.set_log_folder("")
        self.assertEqual("", self.logger.log_folder)
        self.assertTrue(self.logger.enabled)

    def test_set_log_ident_empty(self):
        self.logger.set_log_ident("")
        self.assertEqual("", self.logger.log_ident)
        self.assertTrue(self.logger.enabled)

    def test_reset_time(self):
        time_str = self.logger.timestr
        time.sleep(1)
        self.logger.reset_time()
        self.assertNotEqual(time_str, self.logger.timestr)

    def test_enable(self):
        self.logger.set_log_folder("log_folder")
        self.logger.set_log_ident("log_ident")
        self.logger.enable()
        self.assertTrue(self.logger.enabled)

    def test_enable_both_none(self):
        self.logger.set_log_folder(None)
        self.logger.set_log_ident(None)
        self.logger.enable()
        self.assertFalse(self.logger.enabled)

    def test_enable_folder_none(self):
        self.logger.set_log_folder(None)
        self.logger.set_log_ident("log_ident")
        self.logger.enable()
        self.assertFalse(self.logger.enabled)

    def test_enable_ident_none(self):
        self.logger.set_log_folder("log_folder")
        self.logger.set_log_ident(None)
        self.logger.enable()
        self.assertTrue(self.logger.enabled)
