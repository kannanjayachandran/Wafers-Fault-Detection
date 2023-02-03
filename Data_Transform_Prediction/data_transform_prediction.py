from os import listdir
import pandas as pd
from Application_Logging.application_logger import AppLog


class DataTransformPrediction:
    """
    This class is used for processing the Good Raw data before loading it into the database.(Prediction)
    """
    def __init__(self):
        self.goodDataPath = "Prediction_Raw_Files_Validated/Good_Raw"
        self.logger = AppLog()

    def replacing_missing(self):
        """
        Method Name: replaceMissing
        Description: This method replaces missing values in columns with 'NULL'.
        """
        log_file = open("Prediction_Logs/DataTransformLog.txt", 'a+')
        try:
            all_files = [filename for filename in listdir(self.goodDataPath)]

            for filename in all_files:
                df = pd.read_csv(self.goodDataPath + "/" + filename)
                df.fillna('NULL', inplace=True)
                df['Wafer'] = df['Wafer'].str[6:]

                df.to_csv(self.goodDataPath + "/" + filename, index=None, header=True)
                self.logger.app_logger(log_file, f'{filename}: File transformed successfully.')
        except Exception as e:
            self.logger.app_logger(log_file, f'Data transformation failed {e}')
            log_file.close()

        log_file.close()
