<div align="center">

# Data Preprocessing

</div>

### Data preprocessing is a technique that is used to convert the raw data into a clean data set. In other words, whenever the data is collected from different sources it is likely to contain some errors or may be incomplete. This folder contains two python files

1. preprocessing.py
2. clustering.py

### preprocessing.py

> This file contains the code for cleaning data for training the model. The class is called Preprocessor and it contains the following files:

- `remove_cols(self, data, cols)` - This method is used to remove the columns that are not required for training the model. The output of this method is a pandas dataframe.

- `separate_label_feature(self, data, label_col_name)` - This method is used to separate the features and a Label (All columns except the Label column are treated as features). The output of this method is two dataframes, one containing features and the other containing Labels.

- `is_null_present(self, data)` - This method is used to check if there are any missing values in the data. The output of this method is a boolean value.

- `impute_missing_values(self, data)` - This method is used to impute the missing values in the data. The output of this method is a pandas dataframe which has all the missing values imputed.

- `get_columns_with_zero_std_deviation(self, data)` - This method is used to get the names of all the columns which have a standard deviation of zero. The output of this method is a list of column names.

### clustering.py

> This file contains the code for clustering the data. The class is called KMeansClustering and it contains the following files:
> **We use a module known as kneed to find the optimal number of clusters. Kneed is a Python package that finds the knee point of a curve. This library is an implementation of the Detecting Knee Points in System Behavior paper [paper](https://raghavan.usc.edu//papers/kneedle-simplex11.pdf). Knee point of a functions is simply the point where the rate of change of the function changes drastically.**
> **The elbow method is a heuristic used in determining the number of clusters in a dataset. The method consists of plotting the explained variance as a function of the number of clusters, and picking the elbow of the curve as the number of clusters to use.**
> **I have used KMeans clustering for clustering the data. KMeans clustering is a type of unsupervised learning, which is used when you have unlabeled data (i.e., data without defined categories or groups).**

- `elbow_plot(self, data)` - This method is used to plot the elbow curve to find the optimal number of clusters. The output of this method is a plot.

- `create_clusters(self, data, number_of_clusters)` - This method is used to create clusters using KMeans clustering. The output of this method is a list of clusters. It would also save the model in the models folder.
