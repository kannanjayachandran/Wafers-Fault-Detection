import os
import shutil
import joblib
from Application_Logging.application_logger import AppLog


class FileOperation:
    """
    This class is used to perform file-saving related operations.
    """

    def __init__(self, file_object):
        self.logger = AppLog()
        self.models_dir = os.path.abspath('models')
        self.file_object = file_object

    def save_model(self, model, filename):
        """
        Saves the model file.
        """
        self.logger.app_logger(self.file_object, 'Entered the save_model method of the FileOperation class')
        try:
            path = os.path.join(self.models_dir, filename)
            if os.path.exists(path):
                shutil.rmtree(path)
            os.makedirs(path)

            with open(os.path.join(path, f'{filename}.joblib'), 'wb') as f:
                joblib.dump(model, f)

            self.logger.app_logger(self.file_object, f'Model file {filename} saved.')
            return 'success'

        except Exception as e:
            self.logger.app_logger(self.file_object, f'Error saving model file {filename}: {e}')
            raise

    def load_model(self, filename):
        """
        Loads the model file to memory.
        """
        self.logger.app_logger(self.file_object, 'Entered the load_model method of the FileOperation class')
        try:
            with open(os.path.join(self.models_dir, filename, f'{filename}.joblib'), 'rb') as f:
                model = joblib.load(f)

            self.logger.app_logger(self.file_object, f'Model file {filename} loaded.')
            return model

        except Exception as e:
            self.logger.app_logger(self.file_object, f'Error loading model file {filename}: {e}')
            raise

    def find_correct_model_file(self, cluster_number):
        """
        Selects the correct model based on cluster number.
        """
        self.logger.app_logger(self.file_object, 'Entered the find_correct_model_file method '
                                                 'of the FileOperation class')
        try:
            files = os.listdir(self.models_dir)
            for file in files:
                if str(cluster_number) in file:
                    filename = os.path.splitext(file)[0]
                    self.logger.app_logger(self.file_object, f'Found model file {filename}.')
                    return filename

            self.logger.app_logger(self.file_object, f'No model file found for cluster {cluster_number}.')
            return None

        except Exception as e:
            self.logger.app_logger(self.file_object, f'Error finding model file for cluster {cluster_number}: {e}')
            raise
