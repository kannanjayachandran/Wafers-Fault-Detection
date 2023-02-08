import pandas as pd
from File_Operations import file_methods
from Data_Preprocessing import preprocessing
from Data_Ingestion import data_loader_prediction
from Application_Logging import application_logger
from Prediction_Raw_Data_Validation import Data_Validation


class Prediction:
    def __init__(self, path):
        self.file_object = open("Prediction_Logs/Prediction_Log.txt", 'a+')
        self.log_writer = application_logger.AppLog()

        if path is not None:
            self.prediction_data_value = Data_Validation.PredictionDataValidation(path)

    def predict_from_model(self):

        try:
            self.prediction_data_value.delete_prediction_files()  # deletes the existing prediction file from last run!
            self.log_writer.app_logger(self.file_object, 'Start of Prediction')
            data_getter = data_loader_prediction.DataGetterPrediction(self.file_object, self.log_writer)
            data = data_getter.get_data_prediction()

            # code change
            # wafer_names=data['Wafer']
            # data=data.drop(labels=['Wafer'],axis=1)

            preprocessor = preprocessing.Preprocessor(self.file_object, self.log_writer)
            is_null_present = preprocessor.is_null_present(data)

            if is_null_present:
                data = preprocessor.impute_missing_values(data)

            cols_to_drop = preprocessor.get_columns_with_zero_std_deviation(data)
            data = preprocessor.remove_cols(data, cols_to_drop)

            file_loader = file_methods.FileOperation(self.file_object, self.log_writer)
            kmeans = file_loader.load_model('KMeans')

            clusters = kmeans.predict(data.drop(['Wafer'], axis=1))  # drops the first column for cluster prediction
            data['clusters'] = clusters
            clusters = data['clusters'].unique()
            for i in clusters:
                # selecting all the records of a particular cluster type
                cluster_data = data[data['clusters'] == i]
                # getting all the wafer names
                wafer_names = list(cluster_data['Wafer'])
                # dropping wafer and clusters columns
                cluster_data = data.drop(['Wafer', 'clusters'], axis=1)
                # finding the model name for that cluster
                model_name = file_loader.find_correct_model_file(i)
                # loading the model using the model name
                model = file_loader.load_model(model_name)
                # these are the predicted values
                pred_values = list(model.predict(cluster_data))
                # creating a dataframe with wafer names and predictions
                result = pd.DataFrame(list(zip(wafer_names, pred_values)), columns=['Wafer', 'Prediction'])
                # path to save the dataframe as csv file
                path: str = "Prediction_Output_File/Predictions.csv"
                # writing to csv files
                result.to_csv(path, header=True, mode='a+')  # appends result to prediction file
            self.log_writer.app_logger(self.file_object, 'End of Prediction')
        except Exception as ex:
            self.log_writer.app_logger(self.file_object, 'Error occured while running the prediction!! Error:: %s' % ex)
            raise ex
        return path, result.head().to_json(orient="records")
