from datetime import datetime


class AppLog:
    @staticmethod
    def app_logger(file_obj, log_message):
        """
        Method Name: app_logger
        Description: Logs the message into the log file.

        :param file_obj:
        :param log_message:
        :return:
        """
        now = datetime.now()
        date = now.date()
        current_time = now.strftime("%H:%M:%S")

        log_line = f"{date}-{current_time}\t\t{log_message}\n"
        with open(file_obj, 'a') as f:
            f.write(log_line)
