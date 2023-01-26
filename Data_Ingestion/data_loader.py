import pandas as pd

class Data_getter:
    """
  This class would be used to get data from the source for training
  """
    def __init__(self, file_object, logger_object):
        self.training_file = 'Training_FileFromDB/InputFile.csv'

