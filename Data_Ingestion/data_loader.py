import pandas as pd


class DataGetter:
    """
  This class would be used to get data from the source for training
  """

    def __init__(self, file_object, logger_object):
        self.training_file = 'Training_FileFromDB/InputFile.csv'
        self.file_object = file_object
        self.logger_object = logger_object

    def get_data(self):
        """
        Method Name: get_data
        Description: This methods reads data form the source
        Output: Pandas Dataframe
        """
        self.logger_object.log(self.file_object, 'Inside the get_data method of the DataGetter class')

        try:
            self.data = pd.read_csv(self.training_file)
            self.logger_object.log(self.file_object, 'Data successfully loaded. Exited the get_data method',)

            return self.data
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occurred in get_data method. Exception message: ' + str(e))
            self.logger_object.log(self.file_object,
                                   'Data Loading failed.Exited the get_data method')
            raise Exception()
