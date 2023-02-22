import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from kneed import KneeLocator
from File_Operations.file_methods import FileOperation
from Application_Logging.application_logger import AppLog


class KMeansClustering:
    """
    This class would be used to divide the data into clusters for training.
    """
    def __init__(self, file_object):
        self.save_model = None
        self.file_object = file_object
        self.logger = AppLog()

    def elbow_plot(self, data):
        """
        Method to create an elbow plot and find the optimum number of clusters
        :param data: array-like or dataframe
        :return: int
        """
        self.logger.app_logger(self.file_object, 'Entered the elbow_plot method of the KMeansClustering class')

        WCSS = []  # Empty list for storing the within cluster sum of squares (WCSS)

        try:
            for i in range(1, 11):
                kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)  # initializing the KMeans object
                kmeans.fit(data)  # fitting the data to the KMeans Algorithm
                WCSS.append(kmeans.inertia_)  # appending the WCSS to the list

            plt.plot(range(1, 11), WCSS)  # creating the graph between WCSS and the number of clusters
            plt.title('The Elbow Method')
            plt.xlabel('Number of clusters')
            plt.ylabel('Within Cluster Sum of Squares (WCSS)')

            plt.savefig('preprocessing_data/K-Means_Elbow.PNG')

            # finding the optimum number of clusters using the KneeLocator method from the kneed library
            self.kn = KneeLocator(range(1, 11), WCSS, curve='convex', direction='decreasing')
            self.logger.app_logger(self.file_object, f'The optimum number of clusters is: {self.kn.knee}. Exited the '
                                                     'elbow_plot method of the KMeansClustering class')
            return self.kn.knee
        except Exception as e:
            self.logger.app_logger(self.file_object, 'Exception occurred in elbow plot method of the '
                                                     f'KMeansClustering class. Exception message:  {e}')
            self.logger.app_logger(self.file_object, 'Finding the number of clusters failed. Exited the elbow_plot '
                                                     'method of the KMeansClustering class')
            raise Exception()

    def create_clusters(self, data, number_of_clusters):
        """
        Method to create clusters and add a new column in the dataframe consisting of the cluster information
        :param data: array-like or dataframe
        :param number_of_clusters: int
        :return: dataframe
        """
        self.logger.app_logger(self.file_object, 'Entered the create_clusters method of the KMeansClustering class')

        # Validate inputs
        if not isinstance(data, (list, tuple, set)) and not hasattr(data, 'iloc'):
            raise ValueError("Data must be an array-like or dataframe")
        if not isinstance(number_of_clusters, int) or number_of_clusters <= 0:
            raise ValueError("Number of clusters must be a positive integer")

        try:
            kmeans_model = KMeans(n_clusters=number_of_clusters, init='k-means++', random_state=42)
            cluster_labels = kmeans_model.fit_predict(data)

            # Save the KMeans model to file
            file_operation = FileOperation(self.file_object)
            self.save_model = file_operation.save_model(kmeans_model, 'KMeans')

            # Add cluster information to dataframe
            data['Cluster'] = cluster_labels

            self.logger.app_logger(self.file_object, f'Successfully created {number_of_clusters} clusters. '
                                                     'Exited the create_clusters method of the KMeansClustering class')

            return data

        except Exception as e:
            self.logger.app_logger(self.file_object, 'Exception occurred in create_clusters method of the '
                                                     f'KMeansClustering class: {e}')
            raise ValueError(f"Fitting the data to clusters failed: {e}")
