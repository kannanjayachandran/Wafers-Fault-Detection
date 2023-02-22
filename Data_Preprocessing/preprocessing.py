import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from Application_Logging.application_logger import AppLog


class Preprocessor:
    """
    This class is used for data preprocessing
    """

    def __init__(self, file_object):
        self.logger = AppLog()
        self.file_object = file_object

    def remove_columns(self, data, cols_to_remove):
        """
        Remove the specified columns from a DataFrame.
        :param data: pandas DataFrame
        :param cols_to_remove: list of column names to remove
        :return: pandas DataFrame
        """
        self.logger.app_logger(self.file_object, 'Entered the remove_columns method of the Preprocessor class')
        try:
            useful_data = data.drop(labels=cols_to_remove, axis=1)
            self.logger.app_logger(self.file_object, 'Successfully removed columns. Exited remove_cols method')
            return useful_data
        except KeyError as e:
            self.logger.app_logger(self.file_object, 'Exception occurred in remove_cols method of Preprocessor class'
                                                     f'Exception message: {e}')
            self.logger.app_logger(self.file_object, 'Column removal failed. Exited remove_col method')
            raise

    def separate_label_feature(self, data, label_col_name):
        """
        Separate the label column from the feature columns in a DataFrame.

        :param data: pandas DataFrame
        :param label_col_name: name of the label column
        :return: tuple of two pandas DataFrames (features, labels)
        """
        self.logger.app_logger(self.file_object, 'Entered separate_label_feature method of Preprocessor class')

        try:
            features_x = data.drop(labels=[label_col_name], axis=1)
            labels_y = data[label_col_name]  # filtering the label column
            self.logger.app_logger(self.file_object,
                                   'Successfully separated labels. Exited separate_label_feature method')
            return features_x, labels_y
        except KeyError as e:
            self.logger.app_logger(self.file_object, 'Exception occurred in separate_label_feature method of '
                                                     f'Preprocessor class Exception message: {e}')
            self.logger.app_logger(self.file_object, 'Label separation failed. Exited separate_label_feature method')
            raise

    def has_null_values(self, data):
        """
        Check if the DataFrame contains any missing values.

        :param data: pandas DataFrame
        :return: Boolean
        """
        self.logger.app_logger(self.file_object, 'Entered the has_null_values method of the Preprocessor class')
        if not isinstance(data, pd.DataFrame):
            self.logger.app_logger(self.file_object, 'Input data is not a pandas DataFrame')
            raise ValueError('Input data is not a pandas DataFrame')

        has_nulls = data.isnull().any().sum() > 0
        if has_nulls:
            cols_with_nulls = data.columns[data.isnull().any()].tolist()
            dataframe_with_null = pd.DataFrame()
            dataframe_with_null['columns'] = data.columns
            dataframe_with_null['missing values count'] = np.asarray(data.isna().sum())
            dataframe_with_null.to_csv('preprocessing_data/null_values.csv')
            for col in cols_with_nulls:
                null_percentage = data[col].isnull().sum() / data.shape[0] * 100
                self.logger.app_logger(self.file_object, f"Column '{col}' has {null_percentage:.2f}% null values.")
        else:
            self.logger.app_logger(self.file_object, 'No missing values found')
        self.logger.app_logger(self.file_object, 'Exited the has_null_values method of the Preprocessor class')
        return has_nulls

    def impute_missing_values(self, data):
        """
        Imputes missing values in a Pandas DataFrame using KNN imputation.

        :param data: A Pandas DataFrame with missing values
        :return: A new DataFrame with the missing values imputed using KNN imputation.
        """

        if not isinstance(data, pd.DataFrame):
            self.logger.app_logger(self.file_object, 'Input data is not a pandas DataFrame')
            raise TypeError("Input data must be a Pandas DataFrame")

        try:
            if data.isnull().sum().sum() == 0:
                # No missing values, return original data
                return data

            imputer = KNNImputer(n_neighbors=3, weights='uniform', missing_values=np.nan)
            new_array = imputer.fit_transform(data)
            new_data = pd.DataFrame(data=new_array, columns=data.columns)
            self.logger.app_logger(self.file_object, 'Missing values imputed successfully. Exited the '
                                                     'impute_missing_values method of the Preprocessor class')
            return new_data
        except Exception as e:
            self.logger.app_logger(self.file_object, 'Exception occurred in impute_missing_values method of '
                                                     f'Preprocessor class. Exception message: {e}')
            raise e

    def get_columns_with_zero_std_deviation(self, data):
        """
        Finds out the columns which have a standard deviation of zero.
        :param data: pandas DataFrame
        :return: list of column names
        """
        self.logger.app_logger(self.file_object, 'Entered the get_columns_with_zero_std_deviation method of the '
                                                 'Preprocessor class')
        try:
            columns = data.columns
            data_n = np.std(data, axis=0)
            col_to_drop = []
            for x in columns:
                if data_n[x] == 0:
                    col_to_drop.append(x)
            self.logger.app_logger(self.file_object, f'Found {len(col_to_drop)} columns with zero standard deviation')
            self.logger.app_logger(self.file_object, 'Exited the get_columns_with_zero_std_deviation method of '
                                                     'the Preprocessor class')
            return col_to_drop
        except Exception as e:
            self.logger.app_logger(self.file_object, 'Exception occurred in get_columns_with_zero_std_deviation method '
                                                     f'of the Preprocessor class. Exception message: {str(e)}')
            self.logger.app_logger(self.file_object, 'Column search for Standard Deviation of Zero Failed. Exited '
                                                     'the get_columns_with_zero_std_deviation method of the '
                                                     'Preprocessor class')
            raise ValueError('Failed to find columns with zero standard deviation')
