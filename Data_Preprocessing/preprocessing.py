import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer


class Preprocessor:
    """
    This class is used to clean data for training
    """

    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object

    def remove_cols(self, data, cols):
        """
        Method Name : remove_cols
        Description : This method removes a given column from a dataframe
        Output : Dataframe after removing specified columns
        :param data:
        :param cols:
        """
        self.logger_object.log(self.file_object, 'Entered the remove_cols method of Preprocessor class')
        self.data = data
        self.cols = cols

        try:
            self.useful_data = self.data.drop(labels=self.cols, axis=1)
            # It would drop the label specified in the column
            self.logger_object.log(self.file_object, 'Successfully removed column. Exited remove_cols method')
            return self.useful_data
        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception occurred in remove_cols method of Preprocessor class'
                                                     'Exception message:  ' + str(e))
            self.logger_object.log(self.file_object, 'Column removal failed. Exited remove_col method')

            raise Exception()

    def separate_label_feature(self, data, label_col_name):
        """
        Method Name : separate_label_feature
        Description : This method separates features from label columns
        Output : Two dataframes one containing features, one containing labels
        :param data:
        :param label_col_name:
        :return:
        """

        self.logger_object.log(self.file_object, 'Entered separate_label_feature method of Preprocessor class')

        try:
            self.X = data.drop(labels=label_col_name, axis=1)
            self.Y = data[label_col_name]  # filtering the label columns
            self.logger_object.log(self.file_object, 'Successfully separated labels.' ''
                                                     'Exited separate_label_feature method')
            return self.X, self.Y
        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception occurred in separate_label_feature' ''
                                                     'method of Preprocessor class. Exception message: ' + str(e))
            self.logger_object.log(self.file_object, 'Label separation unsuccessful.'
                                                     'Exited separate_label_feature method')
            raise Exception()

    def is_null_present(self, data):
        """
        Method Name: is_null_present
        Description: This method checks if there is null values in the dataframe
        Output: Returns a Boolean Value.
        :param data:
        :return:
        """

        self.logger_object.log(self.file_object, 'Entered the is_null_present method of the Preprocessor class')
        self.null_present = False

        try:
            self.null_counts = data.isna().sum()  # count of null values per column
            for i in self.null_counts:
                if i > 0:
                    self.null_present = True
                    break

            if (self.null_present):  # writing logs to see which columns have null value
                dataframe_with_null = pd.DataFrame()
                dataframe_with_null['columns'] = data.columns
                dataframe_with_null['missing values count'] = np.asarray(data.isna().sum())
                dataframe_with_null.to_csv('preprocessing_data/null_values.csv')
                # storing the null column information to file

            self.logger_object.log(self.file_object, 'Finding missing values is a success. Data written to the null'
                                                     'values file. Exited the is_null_present method of the'
                                                     'Preprocessor class')
            return self.null_present

        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception occured in is_null_present method of the Preprocessor '
                                                     'class. Exception message: ' + str(e))
            self.logger_object.log(self.file_object, 'Finding missing values failed. Exited the is_null_present '
                                                     'method of the Preprocessor class')
            raise Exception()

    def impute_missing_values(self, data):

        return None