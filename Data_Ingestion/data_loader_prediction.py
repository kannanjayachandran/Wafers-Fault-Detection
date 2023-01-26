import pandas as pd

class DataGetterPrediction:
    """
    This class would be used to get data for prediction
    """

    def __init__(self, file_object, logger_object):
        self.prediction_file = 'Prediction_FileFromDB/InputFile.csv'
        self.file_object = file_object
        self.logger_object = logger_object

    def get_data_prediction(self):

        try:
            self.data = pd.read_csv(self.prediction_file)
            self.logger_object.log(self.file_object, 'Successfully loaded data. Exited the get_data_prediction method')
            return self.data

        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception occurred in get_data_prediction method.',
                                   ' Exception message: '+str(e))
            self.logger_object.log(self.file_object,
                                   'Data Loading failed.Exited the get_data_prediction method ')
            raise Exception()

