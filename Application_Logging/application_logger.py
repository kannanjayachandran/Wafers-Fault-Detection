from datetime import datetime


class AppLog:
    @staticmethod
    def app_logger(file_obj: str, log_message: str) -> None:
        """
        This method logs the messages to the log file.
        :param file_obj: str - path to the log file
        :param log_message: str - message to be logged
        :return: None
        """
        now: datetime = datetime.now()
        date: str = now.date().isoformat()
        current_time: str = now.strftime("%H:%M:%S")

        log_line: str = f"{date}-{current_time}\t\t{log_message}\n"
        with open(file_obj, 'a') as f:
            f.write(log_line)
