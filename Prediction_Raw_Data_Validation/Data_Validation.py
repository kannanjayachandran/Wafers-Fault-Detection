from datetime import datetime
from os import listdir
import os
import re
import json
import shutil
import pandas as pd
from Application_Logging.application_logger import AppLog


class PredictionDataValidation:
    """
       This class shall be used for handling all the validation done on the Raw Prediction Data!!.
    """

    def __init__(self, path):
        self.batch_dir = path
        self.schema_path = 'schema_prediction.json'
        self.logger = AppLog()

    def values_from_schema(self):
        """
        Method Name: values_from_schema
        Description: This method extracts all the relevant information from the pre-defined "Schema" file.
        Output: LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, Number of Columns
        :return:
        """

        try:
            with open(self.schema_path, 'r') as f:
                dic = json.load(f)
                f.close()
            pattern = dic['SampleFileName']

            length_of_date_stamp = dic['LengthOfDateStamp']
            length_of_time_stamp = dic['LengthOfTimeStamp']
            column_names = dic['ColName']
            col_number = dic['ColumnNumber']

            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            message = "LengthOfDateStamp:: %s" % length_of_date_stamp + "\t" + "LengthOfTimeStamp:: %s" \
                      % length_of_time_stamp + "\t " + "ColumnNumber:: %s" % col_number + "\n"

            self.logger.app_logger(file, message)
            file.close()

        except ValueError:
            file = open("Prediction_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.app_logger(file, "ValueError:Value not found inside schema_training.json")
            file.close()
            raise ValueError

        except KeyError:
            file = open("Prediction_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.app_logger(file, "KeyError:Key value error incorrect key passed")
            file.close()
            raise KeyError

        except Exception as e:
            file = open("Prediction_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.app_logger(file, str(e))
            file.close()
            raise e

        return length_of_date_stamp, length_of_time_stamp, column_names, col_number

    def manual_regex_creation(self):

        """
            Method Name: manual_regex_creation
            Description: This method creates a Regex based on the "FileName" given in "Schema" file. It is used
                            to validate the filename of the prediction data.
            Output: Regex pattern
        """
        regex = "['wafer']+['\_'']+[\d_]+[\d]+\.csv"
        return regex

    def create_dir_for_goo_bad_raw_data(self):

        """
            Method Name: create_dir_for_goo_bad_raw_data
            Description: This method creates directories to store the Good Data and Bad Data
                          after validating the prediction data.
            Output: None

        """
        try:
            path = os.path.join("Prediction_Raw_Files_Validated/", "Good_Raw/")
            if not os.path.isdir(path):
                os.makedirs(path)
            path = os.path.join("Prediction_Raw_Files_Validated/", "Bad_Raw/")
            if not os.path.isdir(path):
                os.makedirs(path)

        except OSError as e:
            file = open("Prediction_Logs/GeneralLog.txt", 'a+')
            self.logger.app_logger(file, f'Error while creating Directory {e}')
            file.close()
            raise OSError

    def delete_good_data_training_folder(self):
        """
            Method Name: delete_good_data_training_folder
            Description: This method deletes the directory made to store the Good Data
                          after loading the data in the table. Once the good files are
                          loaded in the DB,deleting the directory ensures space optimization.
            Output: None
        """
        try:
            path = 'Prediction_Raw_Files_Validated/'
            # if os.path.isdir("ids/" + userName):
            # if os.path.isdir(path + 'Bad_Raw/'):
            #     shutil.rmtree(path + 'Bad_Raw/')
            if os.path.isdir(path + 'Good_Raw/'):
                shutil.rmtree(path + 'Good_Raw/')
                file = open("Prediction_Logs/GeneralLog.txt", 'a+')
                self.logger.app_logger(file, "GoodRaw directory deleted successfully!!!")
                file.close()
        except OSError as e:
            file = open("Prediction_Logs/GeneralLog.txt", 'a+')
            self.logger.app_logger(file, f'Error while deleting directory {e}')
            file.close()
            raise OSError

    def delete_bad_data_training_folder(self):

        """
            Method Name: delete_bad_data_training_folder
            Description: This method deletes the directory made to store the bad Data.
            Output: None
        """

        try:
            path = 'Prediction_Raw_Files_Validated/'
            if os.path.isdir(path + 'Bad_Raw/'):
                shutil.rmtree(path + 'Bad_Raw/')
                file = open("Prediction_Logs/GeneralLog.txt", 'a+')
                self.logger.app_logger(file, "BadRaw directory deleted before starting validation!!!")
                file.close()
        except OSError as e:
            file = open("Prediction_Logs/GeneralLog.txt", 'a+')
            self.logger.app_logger(file, f'Error while Deleting Directory {e}:')
            file.close()
            raise OSError

    def move_bad_files_to_bad_archive(self):
        """
            Method Name: move_bad_files_to_bad_archive
            Description: This method deletes the directory made  to store the Bad Data
                          after moving the data in an archive folder. We archive the bad
                          files to send them back to the client for invalid data issue.
            Output: None
        """
        now = datetime.now()
        date = now.date()
        time = now.strftime("%H%M%S")
        try:
            path = "PredictionArchivedBadData"
            if not os.path.isdir(path):
                os.makedirs(path)

            source = 'Prediction_Raw_Files_Validated/Bad_Raw/'
            destination = 'PredictionArchivedBadData/BadData_' + str(date) + "_" + str(time)

            if not os.path.isdir(destination):
                os.makedirs(destination)
            files = os.listdir(source)

            for f in files:
                if f not in os.listdir(destination):
                    shutil.move(source + f, destination)
            file = open("Prediction_Logs/GeneralLog.txt", 'a+')
            self.logger.app_logger(file, "Bad files moved to archive")
            path = 'Prediction_Raw_Files_Validated/'

            if os.path.isdir(path + 'Bad_Raw/'):
                shutil.rmtree(path + 'Bad_Raw/')
            self.logger.app_logger(file, "Bad Raw Data Folder Deleted successfully!!")
            file.close()

        except OSError as e:
            file = open("Prediction_Logs/GeneralLog.txt", 'a+')
            self.logger.app_logger(file, f'Error while moving bad files to archive:: {e}')
            file.close()
            raise OSError

    def validation_file_name_raw(self, regex, LengthOfDateStampInFile, LengthOfTimeStampInFile):
        """
            Method Name: validationFileNameRaw
            Description: This function validates the name of the prediction csv file as per given name in the schema!
                         Regex pattern is used to do the validation.If name format do not match the file is moved
                         to Bad Raw Data folder else in Good raw data.
            Output: None
            On Failure: Exception
        """
        # delete the directories for good and bad data in case last run was unsuccessful and folders were not deleted.
        self.delete_bad_data_training_folder()
        self.delete_good_data_training_folder()
        self.create_dir_for_goo_bad_raw_data()
        only_files = [f for f in listdir(self.batch_dir)]

        try:
            f = open("Prediction_Logs/nameValidationLog.txt", 'a+')

            def copy_to_good_raw(filename):
                shutil.copy("Prediction_Batch_files/" + filename, "Prediction_Raw_Files_Validated/Good_Raw")
                self.logger.app_logger(f, f'Valid File name!! File moved to GoodRaw Folder :: {filename}')

            def copy_to_bad_raw(filename):
                shutil.copy("Prediction_Batch_files/" + filename, "Prediction_Raw_Files_Validated/Bad_Raw")
                self.logger.app_logger(f, f'Invalid File Name!! File moved to Bad Raw Folder :: {filename}')

            for filename in only_files:
                if re.match(regex, filename):
                    split_at_dot = re.split('.csv', filename)
                    split_at_dot = (re.split('_', split_at_dot[0]))
                    if len(split_at_dot[1]) == LengthOfDateStampInFile:
                        if len(split_at_dot[2]) == LengthOfTimeStampInFile:
                            copy_to_good_raw(filename)
                        else:
                            copy_to_bad_raw(filename)
                    else:
                        copy_to_bad_raw(filename)
                else:
                    copy_to_bad_raw(filename)

            f.close()

        except Exception as e:
            f = open("Prediction_Logs/nameValidationLog.txt", 'a+')
            self.logger.app_logger(f, f'Error occured while validating FileName {e}')
            f.close()
            raise e

    def validate_col_len(self, NumberofColumns):
        """
            Method Name: validate_col_len
            Description: This function validates the number of columns in the csv files.
                         It should be same as given in the schema file.
                         If not same file is not suitable for processing and thus is moved to Bad Raw Data folder.
                         If the column number matches, file is kept in Good Raw Data for processing.
                        The csv file is missing the first column name, this function changes the missing name to "Wafer".
            Output: None
        """
        try:
            f = open("Prediction_Logs/columnValidationLog.txt", 'a+')
            self.logger.app_logger(f, "Column Length Validation Started!!")
            for file in listdir('Prediction_Raw_Files_Validated/Good_Raw/'):
                csv = pd.read_csv("Prediction_Raw_Files_Validated/Good_Raw/" + file)

                if csv.shape[1] == NumberofColumns:
                    csv.rename(columns={"Unnamed: 0": "Wafer"}, inplace=True)
                    csv.to_csv("Prediction_Raw_Files_Validated/Good_Raw/" + file, index=None, header=True)
                else:
                    shutil.move("Prediction_Raw_Files_Validated/Good_Raw/" + file,
                                "Prediction_Raw_Files_Validated/Bad_Raw")
                    self.logger.app_logger(f,
                                           f'Invalid Column Length for the file!! File moved to Bad Raw Folder :: {file}')

            self.logger.app_logger(f, "Column Length Validation Completed!!")
        except OSError as e:
            f = open("Prediction_Logs/columnValidationLog.txt", 'a+')
            self.logger.app_logger(f, f'Error Occurred while moving the file :: {e}')
            f.close()
            raise OSError

        except Exception as e:
            f = open("Prediction_Logs/columnValidationLog.txt", 'a+')
            self.logger.app_logger(f, f'Error occurred::{e}')
            f.close()
            raise e

        f.close()

    def delete_prediction_files(self):

        if os.path.exists('Prediction_Output_File/Predictions.csv'):
            os.remove('Prediction_Output_File/Predictions.csv')

    def validate_missing_values_col(self):
        """
            Method Name: validate_missing_values_col
            Description: This function validates if any column in the csv file has all values missing.
                       If all the values are missing, the file is not suitable for processing.
                       SUch files are moved to bad raw data.
            Output: None
        """
        try:
            f = open("Prediction_Logs/missingValuesInColumn.txt", 'a+')
            self.logger.app_logger(f, "Missing Values Validation Started!!")

            for file in listdir('Prediction_Raw_Files_Validated/Good_Raw/'):
                csv = pd.read_csv("Prediction_Raw_Files_Validated/Good_Raw/" + file)
                count = 0
                for columns in csv:
                    if (len(csv[columns]) - csv[columns].count()) == len(csv[columns]):
                        count += 1
                        shutil.move("Prediction_Raw_Files_Validated/Good_Raw/" + file,
                                    "Prediction_Raw_Files_Validated/Bad_Raw")
                        self.logger.app_logger(f,
                                               f'Invalid Column Length for the file!! File moved to Bad Raw Folder :: {file}')
                        break
                if count == 0:
                    csv.rename(columns={"Unnamed: 0": "Wafer"}, inplace=True)
                    csv.to_csv("Prediction_Raw_Files_Validated/Good_Raw/" + file, index=None, header=True)

        except OSError as e:
            f = open("Prediction_Logs/missingValuesInColumn.txt", 'a+')
            self.logger.app_logger(f, f'Error Occured while moving the file :: {e}')
            f.close()
            raise OSError
        except Exception as e:
            f = open("Prediction_Logs/missingValuesInColumn.txt", 'a+')
            self.logger.app_logger(f, f'Error Occurred:: {e}')
            f.close()
            raise e
        f.close()
