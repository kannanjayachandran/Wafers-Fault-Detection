from datetime import datetime

class App_log:

    def __init__(self):
        pass

    def logger(self, file_obj, log_message):

        self.now = datetime.now()
        self.date = datetime.date()
        self.current_time = self.now.strftime("%H:%M:%S")

        file_obj.write(
            str(self.date) + "/" + str(self.current_time) + "\t\t" + log_message + "\n"
        )
