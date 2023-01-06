import datetime
import io
import unittest
from datetime import datetime

from application_logger import App_log


class TestAppLogger(unittest.TestCase):
    def test_log(self):
        # Create a fake file object
        fake_file = io.StringIO()

        # Create an instance of the App_Logger class
        logger = App_log.app_logger()

        # Log a message
        logger.log(fake_file, "This is a log message")

        # Get the current date and time
        now = datetime.now()
        date = now.date()
        current_time = now.strftime("%H:%M:%S")

        # Check that the message was written to the file in the expected format
        self.assertEqual(fake_file.getvalue(), f"{date}/{current_time}\t\tThis is a log message\n")
