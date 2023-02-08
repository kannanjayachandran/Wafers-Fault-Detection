
import os
import re
import json
import shutil
import pandas as pd
from os import listdir
from datetime import datetime
from Application_Logging.application_logger import AppLog


class RawDataValidation:

    """
    This class is used for validating raw data.
    """
    def __init__(self, path):
        self.batch_dir = path
        self.schema_path = 'schema_training.json'
        self.logger = AppLog()

    def values_from_schema(self):
        """
            Method Name: values_from_schema
            Description: This method extracts all the relevant information from the pre-defined "Schema" file.
            Output: LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, Number of Columns
        """
        try:
            with open(self.schema_path, 'r') as f:
                dic = json.load(f)
                f.close()
            pattern = dic['SampleFileName']
            length_of_date_stamp_in_file = dic['LengthOfDateStampInFile']
            length_of_time_stamp_in_file = dic['LengthOfTimeStampInFile']
            column_names = dic['ColName']
            col_num = dic['NumberofColumns']

            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            message ="LengthOfDateStampInFile:: %s" %length_of_date_stamp_in_file + "\t" +\
                     "LengthOfTimeStampInFile:: %s" % length_of_time_stamp_in_file +"\t " +\
                     "NumberofColumns:: %s" % col_num + "\n"

            self.logger.app_logger(file, message)
            file.close()

        except ValueError:
            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.app_logger(file, "ValueError:Value not found inside schema_training.json")
            file.close()
            raise ValueError

        except KeyError:
            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.app_logger(file, "KeyError:Key value error incorrect key passed")
            file.close()
            raise KeyError

        except Exception as e:
            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.app_logger(file, f'Exception occurred: {e}')
            file.close()
            raise e

        return length_of_date_stamp_in_file, length_of_time_stamp_in_file, column_names, col_num

    def manual_regex_creation(self):
        """
            Method Name: manual_regex_creation
            Description: This method contains regex for validating filename.
            Output: Regex pattern
        """
        regex = "['wafer']+['\_'']+[\d_]+[\d]+\.csv"
        return regex

    def create_dir_for_good_bad_raw_data(self):
        """
            Method Name: create_dir_for_good_bad_raw_data
            Description: This method creates directories to store the Good Data and Bad Data
                        after validating the training data.
        """
        try:
            path = os.path.join("Training_Raw_files_validated/", "Good_Raw/")
            if not os.path.isdir(path):
                os.makedirs(path)
            path = os.path.join("Training_Raw_files_validated/", "Bad_Raw/")
            if not os.path.isdir(path):
                os.makedirs(path)

        except OSError as e:
            file = open("Training_Logs/GeneralLog.txt", 'a+')
            self.logger.app_logger(file,f'Error while creating Directory {e}')
            file.close()
            raise OSError

    def delete_good_data_train_dir(self):
        """
            Method Name: delete_good_data_train_dir
            Description: This method deletes the directory made to store the Good Data
        """

        try:
            path = 'Training_Raw_files_validated/'
            if os.path.isdir(path + 'Good_Raw/'):
                shutil.rmtree(path + 'Good_Raw/')
                file = open("Training_Logs/GeneralLog.txt", 'a+')
                self.logger.app_logger(file, "GoodRaw directory deleted successfully")
                file.close()
        except OSError as e:
            file = open("Training_Logs/GeneralLog.txt", 'a+')
            self.logger.app_logger(file, f'Error while deleting directory {e}')
            file.close()
            raise OSError

    def delete_bad_data_train_dir(self):
        """
            Method Name: delete_bad_data_train_dir
            Description: This method deletes the directory made to store the bad Data.
        """
        try:
            path = 'Training_Raw_files_validated/'
            if os.path.isdir(path + 'Bad_Raw/'):
                shutil.rmtree(path + 'Bad_Raw/')
                file = open("Training_Logs/GeneralLog.txt", 'a+')
                self.logger.app_logger(file, "BadRaw directory deleted before starting validation")
                file.close()
        except OSError as e:
            file = open("Training_Logs/GeneralLog.txt", 'a+')
            self.logger.app_logger(file, f'Error while Deleting Directory {e}')
            file.close()
            raise OSError

    def move_bad_files_to_archive(self):
        """
            Method Name: move_bad_files_to_archive
            Description: This method deletes the directory made  to store the Bad Data
                          after moving the data in an archive folder. We archive the bad
                          files to send them back to the client for invalid data issue.
        """
        now = datetime.now()
        date = now.date()
        time = now.strftime("%H%M%S")
        try:

            source = 'Training_Raw_files_validated/Bad_Raw/'
            if os.path.isdir(source):
                path = "TrainingArchiveBadData"
                if not os.path.isdir(path):
                    os.makedirs(path)
                destination = 'TrainingArchiveBadData/BadData_' + str(date)+"_"+str(time)
                if not os.path.isdir(destination):
                    os.makedirs(destination)
                files = os.listdir(source)

                for f in files:
                    if f not in os.listdir(destination):
                        shutil.move(source + f, destination)
                file = open("Training_Logs/GeneralLog.txt", 'a+')
                self.logger.app_logger(file,"Bad files moved to archive")
                path = 'Training_Raw_files_validated/'
                if os.path.isdir(path + 'Bad_Raw/'):
                    shutil.rmtree(path + 'Bad_Raw/')
                self.logger.app_logger(file, "Bad Raw Data Folder Deleted successfully")
                file.close()
        except Exception as e:
            file = open("Training_Logs/GeneralLog.txt", 'a+')
            self.logger.app_logger(file, f'Error while moving bad files to archive:: {e}')
            file.close()
            raise e

    def raw_file_name_validation(self, regex, LengthOfDateStampInFile, LengthOfTimeStampInFile):
        """
            Method Name: raw_file_name_validation
            Description: This function validates the name of the training csv files as per given name in the schema!
                         Regex pattern is used to do the validation.If name format do not match the file is moved
                         to Bad Raw Data folder else in Good raw data.
        """
        # delete the directories for good and bad data in case last run was unsuccessful and folders were not deleted.
        self.delete_bad_data_train_dir()
        self.delete_good_data_train_dir()

        #create new directories
        self.create_dir_for_good_bad_raw_data()

        only_files = [filename for filename in listdir(self.batch_dir)]
        try:
            f = open("Training_Logs/nameValidationLog.txt", 'a+')

            #moves the filename to badraw folder
            def copy_to_bad_raw(filename):
                shutil.copy("Training_Batch_Files/" + filename, "Training_Raw_files_validated/Bad_Raw")
                self.logger.app_logger(f, f'Invalid File Name!! File moved to Bad Raw Folder :: {filename}')

            def copy_to_good_raw(filename):
                shutil.copy("Training_Batch_Files/" + filename, "Training_Raw_files_validated/Good_Raw")
                self.logger.app_logger(f, f'Valid File name!! File moved to GoodRaw Folder :: {filename}')

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
            f = open("Training_Logs/nameValidationLog.txt", 'a+')
            self.logger.app_logger(f, f'Error occured while validating FileName {e}')
            f.close()
            raise e

    def validate_col_len(self, col_number):
        """
            Method Name: validate_col_number
            Description: This function validates the number of columns in the csv files.
                       It should be same as given in the schema file.
                       If not same file is not suitable for processing and thus is moved to Bad Raw Data folder.
                       If the column number matches, file is kept in Good Raw Data for processing.
                       The csv file is missing the first column name, this function changes the missing name to "Wafer".
        """
        try:
            f = open("Training_Logs/columnValidationLog.txt", 'a+')
            self.logger.app_logger(f, "Column Length Validation Started!!")
            for file in listdir('Training_Raw_files_validated/Good_Raw/'):
                df = pd.read_csv("Training_Raw_files_validated/Good_Raw/" + file)
                if df.shape[1] != col_number:

                    shutil.move("Training_Raw_files_validated/Good_Raw/" + file, "Training_Raw_files_validated/Bad_Raw")
                    self.logger.app_logger(f, f'Invalid Column Length for the file!! File moved to Bad Raw Folder :: {file}')

            self.logger.app_logger(f, "Column Length Validation Completed!!")
        except OSError as e:
            f = open("Training_Logs/columnValidationLog.txt", 'a+')
            self.logger.app_logger(f, f'Error Occured while moving the file :: {e}')
            f.close()
            raise OSError
        except Exception as e:
            f = open("Training_Logs/columnValidationLog.txt", 'a+')
            self.logger.app_logger(f, f'Error Occurred:: {e}')
            f.close()
            raise e
        f.close()

    def validate_missing_values(self):
        """
            Method Name: validate_missing_values
            Description: This function validates if any column in the csv file has all values missing.
                       If all the values are missing, the file is not suitable for processing.
                       SUch files are moved to bad raw data.
        """
        try:
            f = open("Training_Logs/missingValuesInColumn.txt", 'a+')
            self.logger.app_logger(f, "Missing Values Validation Started!!")

            for file in listdir('Training_Raw_files_validated/Good_Raw/'):
                df = pd.read_csv("Training_Raw_files_validated/Good_Raw/" + file)
                count = 0
                for columns in df:
                    if (len(df[columns]) - df[columns].count()) == len(df[columns]):
                        count += 1
                        shutil.move("Training_Raw_files_validated/Good_Raw/" + file,
                                    "Training_Raw_files_validated/Bad_Raw")
                        self.logger.app_logger(f, f'Invalid Column Length for the file!! File moved to Bad Raw Folder :: {file}')
                        break

                if count == 0:
                    df.rename(columns={"Unnamed: 0": "Wafer"}, inplace=True)
                    df.to_csv("Training_Raw_files_validated/Good_Raw/" + file, index=None, header=True)
        except OSError as e:
            f = open("Training_Logs/missingValuesInColumn.txt", 'a+')
            self.logger.app_logger(f, f'Error Occured while moving the file :: {e}')
            f.close()
            raise OSError
        except Exception as e:
            f = open("Training_Logs/missingValuesInColumn.txt", 'a+')
            self.logger.app_logger(f, f'Error Occured:: {e}')
            f.close()
            raise e
        f.close()
