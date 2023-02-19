import pandas as pd
from Application_Logging.application_logger import AppLog


class DataGetter:
    """
    This class is used to get data from a source for training and prediction
    """
    def __init__(self, file_path, file_object):
        self.data = None
        self.file_path = file_path
        self.file_object = file_object
        self.logger = AppLog()

    def get_data(self):
        """
        Method Name: get_data
        Description: This method reads data form the source
        Output: Pandas Dataframe
        :return: data
        :rtype: pandas.DataFrame
        """
        self.logger.app_logger(self.file_object, "Inside the get_data method of the DataGetter class")

        try:
            self.data = pd.read_csv(self.file_path)
            self.logger.app_logger(self.file_object, "Data successfully loaded. Exited the get_data method")
            return self.data

        except FileNotFoundError as e:
            self.logger.app_logger(self.file_object, f"File not found at {self.file_path}. Exception message: {e}")

            raise
        except Exception as e:
            self.logger.app_logger(self.file_object, f"Exception occurred in get_data method. Exception message: {e}")
            self.logger.app_logger(self.file_object, "Data loading failed. Exited the get_data method")
            return None
