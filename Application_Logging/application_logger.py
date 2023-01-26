from datetime import datetime


class AppLog:
    def __init__(self):
        self.date = None
        self.now = None
        self.current_time = None

    def app_logger(self, file_obj, log_message):
        """
        Method Name: app_logger

        :param file_obj:
        :param log_message:
        :return:
        """
        self.now = datetime.now()
        self.date = self.now.date()
        self.current_time = self.now.strftime("%H:%M:%S")

        file_obj.write(
            str(self.date) + "-" + str(self.current_time) + "\t\t" + log_message + "\n"
        )
