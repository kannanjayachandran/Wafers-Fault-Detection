from Application_Logging.application_logger import AppLog
import joblib
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


class BestModel:
    """
    A class to find the best model and hyperparameters, train the model, and evaluate it on test data.
    """

    def __init__(self, x_train, y_train, x_test, y_test, file_object):
        self.best_pipeline = None
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test
        self.file_object = file_object
        self.logger = AppLog()

    def find_best_pipeline(self):
        """
        Find the best model and hyperparameters using cross-validation.
        :return: best pipeline
        """
        try:
            # Define the pipeline for the random forest classifier.
            rf_pipeline = Pipeline([
                ('scaler', StandardScaler()),
                ('rf', RandomForestClassifier())
            ])

            # Define the pipeline for the XGBoost classifier.
            xgb_pipeline = Pipeline([
                ('scaler', StandardScaler()),
                ('xgb', XGBClassifier())
            ])

            # Perform cross-validation on both pipelines and get the scores.
            rf_scores = cross_validate(rf_pipeline, self.x_train, self.y_train,
                                       scoring='accuracy', cv=5, n_jobs=-1)
            xgb_scores = cross_validate(xgb_pipeline, self.x_train, self.y_train,
                                        scoring='accuracy', cv=5, n_jobs=-1)

            # Logging the scores.
            self.logger.app_logger(self.file_object, f'Random Forest scores: {rf_scores}')
            self.logger.app_logger(self.file_object, f'XGBoost scores: {xgb_scores}')

            # Get the mean accuracy scores for each pipeline.
            rf_mean_score = rf_scores['test_score'].mean()
            xgb_mean_score = xgb_scores['test_score'].mean()

            # Logging the mean scores.
            self.logger.app_logger(self.file_object, f'Random Forest mean score: {rf_mean_score}')
            self.logger.app_logger(self.file_object, f'XGBoost mean score: {xgb_mean_score}')

            # Choose the best pipeline based on the mean accuracy score.
            if rf_mean_score > xgb_mean_score:
                self.best_pipeline = rf_pipeline
            else:
                self.best_pipeline = xgb_pipeline

            # Get the best hyperparameters for the chosen pipeline using grid search.
            if self.best_pipeline == rf_pipeline:
                params = {'rf__n_estimators': [10, 50, 100],
                          'rf__max_depth': [5, 10, 20]}
            else:
                params = {'xgb__n_estimators': [10, 50, 100],
                          'xgb__max_depth': [5, 10, 20]}

            # Logging the best hyperparameters.
            self.logger.app_logger(self.file_object, f'Best hyperparameters: {params}')

            self.best_pipeline.fit(self.x_train, self.y_train)
            return self.best_pipeline

        except Exception as e:
            self.logger.app_logger(self.file_object, 'Exception occurred in find_best_pipeline method of the ' +
                                   f'BestModel class. Exception message: {e}')

    def train_best_model(self):
        """
        Train the best model with the best hyperparameters on the entire training set.
        """
        try:
            self.best_pipeline.fit(self.x_train, self.y_train)
        except Exception as e:
            self.logger.app_logger(self.file_object, 'Exception occurred in train_best_model method of the ' +
                                   f'BestModel class. Exception message: {e}')

    def evaluate_best_model(self):
        """
        Evaluate the best model on the test set and return the accuracy score.
        """
        try:
            y_prediction = self.best_pipeline.predict(self.x_test)
            accuracy = (y_prediction == self.y_test).mean()
            return accuracy

        except Exception as e:
            self.logger.app_logger(self.file_object, 'Exception occurred in evaluate_best_model method of the ' +
                                   f'BestModel class. Exception message: {e}')

    def save_model(self, model_path):
        """
        Save the trained model to a file using joblib.
        """
        try:
            joblib.dump(self.best_pipeline, model_path)

        except Exception as e:
            self.logger.app_logger(self.file_object, 'Exception occurred in save_model method of the ' +
                                   f'BestModel class. Exception message: {e}')

    def load_model(self, model_path):
        """
        Load a trained model from a file using joblib.
        """
        try:
            self.best_pipeline = joblib.load(model_path)

        except Exception as e:
            self.logger.app_logger(self.file_object, 'Exception occurred in load_model method of the ' +
                                   f'BestModel class. Exception message: {e}')
