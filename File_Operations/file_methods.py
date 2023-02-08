import pickle
import os
import shutil


class FileOperation:
    """
    This class would be used to perform file-saving related operations.
    It would be used to save the model after training, and to load the model for prediction.
    """

    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object
        self.model_dir = 'models/'

    def save_model(self, model, filename):
        """
        Method Name: save_model
        Description: Save the model file
        Outcome: File gets saved
        :param model:
        :param filename:
        :return:
        """
        self.logger_object.log(self.file_object, 'Entered the save_model method of the File_Operation class')
        try:
            path = os.path.join(self.model_dir, filename)  # create separate directory for each cluster
            if os.path.isdir(path):  # remove previously existing models for each clusters
                shutil.rmtree(self.model_dir)  # remove all the subdirectories!
            os.makedirs(path)

            with open(path + '/' + filename + '.sav', 'wb') as f:
                pickle.dump(model, f)  # save the model to file
            self.logger_object.log(self.file_object, 'Model File ' + filename + ' saved. Exited the save_model method '
                                                                                'of the Model_Finder class')
            return 'success'

        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occurred in save_model method of the Model_Finder class. '
                                   'Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,
                                   'Model File ' + filename + ' could not be saved. Exited the save_model method '
                                                              'of the Model_Finder class')
            raise Exception()

    def load_model(self, filename):
        """
            Method Name: load_model
            Description: load the model file to memory
            Output: The Model file loaded in memory
            On Failure: Raise Exception
        """
        self.logger_object.log(self.file_object, 'Entered the load_model method of the File_Operation class')
        try:
            with open(self.model_dir + filename + '/' + filename + '.sav', 'rb') as f:
                self.logger_object.log(self.file_object, 'Model File ' + filename + ' loaded. Exited the load_model '
                                                                                    'method of the Model_Finder class')
                return pickle.load(f)

        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occurred in load_model method of the Model_Finder class. '
                                   'Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,
                                   'Model File ' + filename + ' could not be saved. Exited the load_model method of '
                                                              'the Model_Finder class')
            raise Exception()

    def find_correct_model_file(self, cluster_number):
        """
            Method Name: find_correct_model_file
            Description: Select the correct model based on cluster number
            Output: The Model file
            On Failure: Raise Exception
        """
        self.logger_object.log(self.file_object,
                               'Entered the find_correct_model_file method of the File_Operation class')
        try:
            self.cluster_number = cluster_number
            self.folder_name = self.model_dir
            self.list_of_model_files = []
            self.list_of_files = os.listdir(self.folder_name)
            for self.file in self.list_of_files:
                try:
                    if (self.file_object.index(str(self.cluster_number)) != -1):
                        self.model_name = self.file_object
                except:
                    continue
            self.model_name = self.model_name.split('.')[0]
            self.logger_object.log(self.file_object,
                                   'Exited the find_correct_model_file method of the Model_Finder class.')
            return self.model_name
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in find_correct_model_file method of the Model_Finder class. '
                                   'Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,
                                   'Exited the find_correct_model_file method of the Model_Finder class with Failure')
            raise Exception()
