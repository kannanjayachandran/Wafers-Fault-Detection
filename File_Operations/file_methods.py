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
