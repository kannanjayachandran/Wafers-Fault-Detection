<div align="center">

# Data Preprocessing

</div>

### Data preprocessing is a technique that is used to convert the raw data into a clean data set. In other words, whenever the data is collected from different sources it is likely to contain some errors or may be incomplete. This folder contains one file

### preprocessing.py

> This folder contains the class and methods used to preprocess the data. The class is called Preprocessor and it contains the following methods:

- remove_cols(self, data, cols) - This method is used to remove the columns that are not required for training the model. The output of this method is a pandas dataframe.

- separate_label_feature(self, data, label_col_name) - This method is used to separate the features and a Label (All columns except the Label column are treated as features). The output of this method is two dataframes, one containing features and the other containing Labels.

- is_null_present(self, data) - This method is used to check if there are any missing values in the data. The output of this method is a boolean value.

- impute_missing_values(self, data) - This method is used to impute the missing values in the data. The output of this method is a pandas dataframe which has all the missing values imputed.
