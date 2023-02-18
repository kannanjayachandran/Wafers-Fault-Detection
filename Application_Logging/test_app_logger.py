import unittest
import os
from application_logger import AppLog


class TestAppLog(unittest.TestCase):
    def setUp(self):
        self.log_file = "test.log"
        self.logger = AppLog()

    def test_app_logger(self):
        log_message = "Test message"
        self.logger.app_logger(self.log_file, log_message)
        with open(self.log_file) as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 1)
            self.assertIn(log_message, lines[0])

    def tearDown(self):
        os.remove(self.log_file)


if __name__ == '__main__':
    unittest.main()
