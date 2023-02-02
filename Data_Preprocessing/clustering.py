import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from kneed import KneeLocator
from File_Operations import file_methods


class KMeansClustering:
    """
    This class would be used to divide the data into clusters for training.
    """

    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object

    def elbow_plot(self, data):
        self.logger_object.log(self.file_object, 'Entered the elbow_plot method of the KMeansClustering class')
        WCSS = []  # Empty list for storing the within cluster sum of squares (WCSS)

        try:
            for i in range(1, 11):
                kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)  # initializing the KMeans object
                kmeans.fit(data)  # fitting the data to the KMeans Algorithm
                WCSS.append(kmeans.inertia_)  # appending the WCSS to the list

            plt.plot(range(1, 11), WCSS)  # creating the graph between WCSS and the number of clusters
            plt.title('The Elbow Method')
            plt.xlabel('Number of clusters')
            plt.ylabel('WCSS')

            plt.savefig('preprocessing_data/K-Means_Elbow.PNG')

            # finding the optimum number of clusters using the KneeLocator method from the kneed library
            self.kn = KneeLocator(range(1, 11), WCSS, curve='convex', direction='decreasing')
            self.logger_object.log(self.file_object, f'The optimum number of clusters is: {self.kn.knee}. Exited the '
                                                     'elbow_plot method of the KMeansClustering class')
            return self.kn.knee
        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception occurred in elbow plot method of the '
                                                     f'KMeansClustering class. Exception message:  {e}')
            self.logger_object.log(self.file_object, 'Finding the number of clusters failed. Exited the elbow_plot '
                                                     'method of the KMeansClustering class')
            raise Exception()

    def create_clusters(self, data, number_of_clusters):
        """
        Method Name: create_clusters
        Description: This method creates a new column in the dataframe consisting of the cluster information.
        Output: A dataframe with cluster column
        :param data:
        :param number_of_clusters:
        :return:
        """

        self.logger_object.log(self.file_object, 'Entered the create_clusters method of the KMeansClustering class')
        self.data = data
        try:
            self.kmeans = KMeans(n_clusters=number_of_clusters, init='k-means++', random_state=42)
            self.y_kmeans = self.kmeans.fit_predict(data)  # divide data into clusters

            self.file_operation = file_methods.FileOperation(self.file_object, self.logger_object)
            self.save_model = self.file_operation.save_model(self.kmeans, 'KMeans')

            # passing 'Model' as the functions need three parameters
            self.data['Cluster'] = self.y_kmeans  # create a new column in dataset for storing the cluster information
            self.logger_object.log(self.file_object, f'Successfully created {self.kn.knee} Clusters. Exited the '
                                                     'create_clusters method of the KMeansClustering class')
            return self.data

        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception occurred in create_clusters method of the '
                                                     f'KMeansClustering class. Exception message:  {e}')
            self.logger_object.log(self.file_object, 'Fitting the data to clusters failed. Exited the create_clusters '
                                                     'method of the KMeansClustering class')
            raise Exception()
