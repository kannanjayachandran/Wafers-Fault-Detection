from Application_Logging.application_logger import AppLog
import json





class DataValidationPrediction:
    """
    This class is used for validating raw data
    """

    def __init__(self, path):
        self.BatchDir = path
        self.schemaPath = 'Training_Schema.json'
        self.logger = AppLog()

    def valuesFromSchema(self):
        """
        This method is used to extract the values from the schema file

        Output: Column_names, Number of Columns, LengthOfDateStampInFile, LengthOfTimeStampInFile

        """
        try:
            with open(self.schemaPath, 'r') as f:
                dic = json.load(f)
                f.close()
            LengthOfDateStampInFile = dic['LengthOfDateStampInFile']
            LengthOfTimeStampInFile = dic['LengthOfTimeStampInFile']
            column_names = dic['ColName']
            NumberofColumns = dic['NumberofColumns']


        return LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, NumberofColumns

    def RegexCreator(self):
        """
        This function contains a Regex that is used to validate the filename of the prediction data,
        based on the "FileName" given in "Schema" file
        """
        regex = "['wafer']+['\_'']+[\d_]+[\d]+\.csv"
        return regex