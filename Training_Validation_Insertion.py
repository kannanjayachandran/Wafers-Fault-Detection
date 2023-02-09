from Training_Raw_data_validation.Training_Raw_data import RawDataValidation
from Data_Type_Validation_Insertion_Training.DataTypeValidationTraining import DBOperation
from Data_Transform_Training.data_transformation import DataTransform
from Application_Logging.application_logger import AppLog


class Train_Validation:
    def __init__(self, path):
        self.raw_data = RawDataValidation(path)
        self.dataTransform = DataTransform()
        self.dBOperation = DBOperation()
        self.file_object = open("Training_Logs/Training_Main_Log.txt", 'a+')
        self.log_writer = AppLog()

    def train_validation(self):
        try:
            self.log_writer.app_logger(self.file_object, 'Start of Validation on files!!')
            # extracting values from prediction schema
            length_of_date_stamp_in_file, length_of_time_stamp_in_file, column_names, num_of_columns = self.raw_data.values_from_schema()
            # getting the regex defined to validate filename
            regex = self.raw_data.manual_regex_creation()
            # validating filename of prediction files
            self.raw_data.raw_file_name_validation(regex, length_of_date_stamp_in_file, length_of_time_stamp_in_file)
            # validating column length in the file
            self.raw_data.validate_col_len(num_of_columns)
            # validating if any column has all values missing
            self.raw_data.validate_missing_values()
            self.log_writer.app_logger(self.file_object, "Raw Data Validation Complete!!")

            self.log_writer.app_logger(self.file_object, "Starting Data Transforamtion!!")
            # replacing blanks in the csv file with "Null" values to insert in table
            self.dataTransform.replacing_missing()

            self.log_writer.app_logger(self.file_object, "DataTransformation Completed!!!")

            self.log_writer.app_logger(self.file_object,"Creating Training_Database and tables on the basis of given schema!!!")
            # create database with given name, if present open the connection! Create table with columns given in schema
            self.dBOperation.db_create_table('Training', column_names)
            self.log_writer.app_logger(self.file_object, "Table creation Completed!!")
            self.log_writer.app_logger(self.file_object, "Insertion of Data into Table started!!!!")
            # insert csv files in the table
            self.dBOperation.insert_into_table_good_data('Training')
            self.log_writer.app_logger(self.file_object, "Insertion in Table completed!!!")
            self.log_writer.app_logger(self.file_object, "Deleting Good Data Folder!!!")
            # Delete the good data folder after loading files in table
            self.raw_data.delete_good_data_train_dir()
            self.log_writer.app_logger(self.file_object, "Good_Data folder deleted!!!")
            self.log_writer.app_logger(self.file_object, "Moving bad files to Archive and deleting Bad_Data folder!!!")
            # Move the bad files to archive folder
            self.raw_data.move_bad_files_to_archive()
            self.log_writer.app_logger(self.file_object, "Bad files moved to archive!! Bad folder Deleted!!")
            self.log_writer.app_logger(self.file_object, "Validation Operation completed!!")
            self.log_writer.app_logger(self.file_object, "Extracting csv file from table")
            # export data in table to csvfile
            self.dBOperation.select_data_from_csv_to_table('Training')
            self.file_object.close()

        except Exception as e:
            raise e
