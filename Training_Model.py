from sklearn.model_selection import train_test_split
from Data_Ingestion import data_loader
from Data_Preprocessing import preprocessing, clustering
from Best_Model_Finder.Best_model import BestModel
from File_Operations.file_methods import FileOperation
from Application_Logging.application_logger import AppLog


class TrainModel:
    def __init__(self):
        self.log_writer = AppLog()
        self.file_object = open("Training_Logs/ModelTrainingLog.txt", 'a+')

    def training_model(self):
        # Logging the start of Training
        self.log_writer.app_logger(self.file_object, 'Start of Training')
        try:
            # Getting the data from the source
            data_getter = data_loader.DataGetter(self.file_object, self.log_writer)
            data = data_getter.get_data()

            # Processing data

            preprocessor = preprocessing.Preprocessor(self.file_object, self.log_writer)
            # remove the unnamed column as it doesn't contribute to prediction.
            data = preprocessor.remove_cols(data, ['Wafer'])

            # create separate features and labels
            x, y = preprocessor.separate_label_feature(data, label_col_name='Output')

            # check if missing values are present in the dataset
            is_null_present = preprocessor.is_null_present(x)

            # if missing values are there, replace them appropriately.
            if is_null_present:
                x = preprocessor.impute_missing_values(x)  # missing value imputation

            cols_to_drop = preprocessor.get_columns_with_zero_std_deviation(x)

            # drop the columns obtained above
            if len(cols_to_drop) > 0:
                x = preprocessor.remove_cols(x, cols_to_drop)

            # Clustering

            kmeans = clustering.KMeansClustering(self.file_object, self.log_writer)  # object initialization.
            number_of_clusters = kmeans.elbow_plot(x)  # using the elbow plot to find the number of optimum clusters

            # Divide the data into clusters and 'Cluster' column be added specifying the cluster number
            x = kmeans.create_clusters(x, number_of_clusters)

            # create a new column in the dataset consisting of the corresponding cluster assignments.
            x['Labels'] = y

            # getting the unique clusters from our dataset
            list_of_clusters = x['Cluster'].unique()

            # parsing all the clusters and looking for the best ML algorithm to fit on individual cluster

            for i in list_of_clusters:
                cluster_data = x[x['Cluster'] == i]  # selecting all the rows of a particular cluster

                # Prepare the feature and Label columns
                cluster_features = cluster_data.drop(['Labels', 'Cluster'], axis=1)
                cluster_label = cluster_data['Labels']

                # splitting the data into training and test set for each cluster one by one
                x_train, x_test, y_train, y_test = train_test_split(cluster_features, cluster_label, test_size=1 / 3, random_state=355)

                model_finder = BestModel(self.file_object,self.log_writer)  # object initialization

                # getting the best model for each of the clusters using hyperparameter tuning
                best_model_name, best_model = model_finder.best_model(x_train, y_train, x_test, y_test)

                # saving the best model to the directory.
                file_op = FileOperation(self.file_object, self.log_writer)
                save_model = file_op.save_model(best_model, best_model_name + str(i))

                return save_model

            # logging the successful Training
            self.log_writer.app_logger(self.file_object, 'Successful End of Training')
            self.file_object.close()

        except Exception:
            # logging the unsuccessful Training
            self.log_writer.app_logger(self.file_object, 'Unsuccessful End of Training')
            self.file_object.close()
            raise Exception
