import unittest
import os
from application_logger import AppLog


class TestAppLog(unittest.TestCase):
    def setUp(self) -> None:
        self.log_file: str = "test.log"
        self.logger: AppLog = AppLog()

    def test_app_logger(self) -> None:
        log_message: str = "Test message"
        self.logger.app_logger(self.log_file, log_message)
        with open(self.log_file) as f:
            lines: List[str] = f.readlines()
            self.assertEqual(len(lines), 1)
            self.assertIn(log_message, lines[0])

    def tearDown(self) -> None:
        os.remove(self.log_file)


if __name__ == '__main__':
    unittest.main()
