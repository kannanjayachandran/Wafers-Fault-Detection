import shutil
import _sqlite3
import os
from os import listdir
import csv
from Application_Logging.application_logger import AppLog


class DBOperation:
    """
    Class for handling SQL related Operations
    """

    def __init__(self):
        self.path = 'Prediction_Database/'
        self.bad_files_path = 'Prediction_Raw_Files_Validated/Bad_Raw_Files'
        self.good_files_path = 'Prediction_Raw_Files_Validated/Good_Raw_Files'
        self.logger = AppLog()

    def database_connection(self, database_name):
        """
        Method Name : database_connection
        Description : This method creates a database with the given name and if the database already exists;
                      then it opens a connection to the database.
        Output : Connect to the database
        :param database_name:
        :return:
        """

        try:
            connections = _sqlite3.connect(self.path + database_name + '.db')
            file = open("Prediction_Logs/DatabaseConnectionLog.txt", 'a+')
            self.logger.app_logger(file, f'Opened {database_name} database successfully')
            file.close()
        except ConnectionError:
            file = open("Prediction_Logs/DatabaseConnectionLog.txt", 'a+')
            self.logger.app_logger(file, f'Error while connecting to the database: {ConnectionError}')
            file.close()
            raise ConnectionError
        return connections

    def db_create_table(self, database_name, column_names):

        """
        Method Name : db_create_table
        Description : This method creates a table in the given database which will be used to
                    insert the Good data after raw data validation.
        Output : A table in the given database
        :param database_name:
        :param column_names:
        :return:
        """

        try:
            connection = self.database_connection(database_name)
            connection.execute('DROP TABLE IF EXISTS Good_Raw_Data;')

            for key in column_names.keys():
                types = column_names[key]
                # we will remove the column of string datatype before loading as it is not needed for training
                # in try block we check if the table exists, if yes then add columns to the table
                # else in catch block we create the table
                try:
                    connection.execute(
                        'ALTER TABLE Good_Raw_Data ADD COLUMN "{column_name}" {dataType}'.format(column_name=key,
                                                                                                 dataType=type))
                except:
                    connection.execute(
                        'CREATE TABLE  Good_Raw_Data ({column_name} {dataType})'.format(column_name=key, dataType=type))

            connection.close()

            file = open("Prediction_Logs/DbTableCreateLog.txt", 'a+')
            self.logger.app_logger(file, "Successfully created Table.")
            file.close()

            file = open("Prediction_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.app_logger(file, f'Closed {database_name} database successfully.')
            file.close()

        except Exception as e:
            file = open("Prediction_Logs/DbTableCreateLog.txt", 'a+')
            self.logger.app_logger(file, f'Error while creating table {e}')
            file.close()
            connection.close()

            file = open("Prediction_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.app_logger(file, f'Closed {database_name} database successfully.')
            file.close()
            raise e

    def insert_into_table_good_data(self, database):
        """
        Method Name : insert_into_table_good_data
        Description : This method inserts the Good data files from the Good_Raw folder into the above created table
        :param database:
        :return:
        """

        connection = self.db_create_table(database)
        good_files_path = self.good_files_path
        bad_files_path = self.bad_files_path

        good_files = [f for f in listdir(good_files_path)]
        log_file = open("Prediction_Logs/DbInsertLog.txt", 'a+')

        for file in good_files:
            try:
                with open(good_files_path + '/' + file, "r") as f:
                    next(f)
                    reader = csv.reader(f, delimiter="\n")

                    for line in enumerate(reader):
                        for list_ in (line[1]):
                            try:
                                connection.execute('INSERT INTO Good_Raw_Data values ({values})'.format(values=(list_)))
                                self.logger.app_logger(log_file, f'{file} : File loaded successfully.')
                                connection.commit()
                            except Exception as e:
                                raise e

            except Exception as e:

                connection.rollback()
                self.logger.app_logger(log_file, f'Error while creating table: {e}')
                shutil.move(good_files_path + '/' + file, bad_files_path)
                self.logger.app_logger(log_file, f'File moved successfully {file}')
                log_file.close()
                connection.close()
                raise e

        connection.close()
        log_file.close()

    def select_data_from_csv_to_table(self, database):
        """
        Method Name : select_data_from_csv_to_table
        Description : This method exports the data in GoodData folder into the table
        :param database:
        :return:
        """

        self.file_from_db = 'Prediction_FileFromDB/'
        self.file_name = 'InputFile.csv'
        log_file = open("Prediction_Logs/ExportToCsv.txt", 'a+')

        try:
            connections = self.database_connection(database)
            sqlSelect = "SELECT *  FROM Good_Raw_Data"
            cursor = connections.cursor()

            cursor.execute(sqlSelect)

            results = cursor.fetchall()

            # Get the headers of the csv file
            headers = [i[0] for i in cursor.description]

            # Make the CSV output directory
            if not os.path.isdir(self.file_from_db):
                os.makedirs(self.file_from_db)

            # Open CSV file for writing.
            csv_file = csv.writer(open(self.file_from_db + self.file_name, 'w', newline=''), delimiter=',',
                                  lineterminator='\r\n', quoting=csv.QUOTE_ALL, escapechar='\\')

            # Add the headers and data to the CSV file.
            csv_file.writerow(headers)
            csv_file.writerows(results)

            self.logger.app_logger(log_file, "Successfully exported file.")

        except Exception as e:
            self.logger.app_logger(log_file, f'File exporting failed. Error {e}')
            raise e
