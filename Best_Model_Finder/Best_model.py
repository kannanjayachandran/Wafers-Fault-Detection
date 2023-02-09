from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score, accuracy_score


class BestModel:
    """
    This class would be used to find the best model in-terms of accuracy and AUC score
    """

    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object
        self.classifier = RandomForestClassifier()
        self.xg_boost = XGBClassifier(objective='binary:logistic')

    def best_parameter_random_forest(self, train_x, train_y):
        """
        Method Name: best_parameter_random_forest
        Description: get the parameters for Random Forest Algorithm which give the best accuracy.
                    Use Hyper Parameter Tuning.
            Output: The model with the best parameters
        :param train_x:
        :param train_y:
        :return:
        """

        self.logger_object.log(self.file_object, 'Entered the best_parameter_random_forest '
                                                 'method of the BestModel class')
        try:
            self.grid_param_random_forest = {
                "n_estimators": [10, 50, 100, 130],
                "criterion": ['gini', 'entropy'],
                "max_depth": range(2, 4, 1),
                "max_features": ['auto', 'log2']
            }

            # Creating an object of the Grid Search class
            self.grid = GridSearchCV(estimator=self.classifier, param_grid=self.grid_param_random_forest, cv=5, verbose=3)
            # finding the best parameters
            self.grid.fit(train_x, train_y)

            # extracting the best parameters
            self.criterion = self.grid.best_params_['criterion']
            self.max_depth = self.grid.best_params_['max_depth']
            self.max_features = self.grid.best_params_['max_features']
            self.n_estimators = self.grid.best_params_['n_estimators']

            # creating a new model with the best parameters
            self.classifier = RandomForestClassifier(n_estimators=self.n_estimators, criterion=self.criterion,
                                                     max_depth=self.max_depth, max_features=self.max_features)
            # training the mew model
            self.classifier.fit(train_x, train_y)
            self.logger_object.log(self.file_object, 'Random Forest best params: ' + str(self.grid.best_params_) +
                                   '. Exited the best_parameter_random_forest method of the BestModel class')

            return self.classifier
        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception occurred in best_parameter_random_forest '
                                                     f'method of the BestModel class. Exception message: {e}')
            self.logger_object.log(self.file_object, 'Random Forest Parameter tuning failed. Exited the '
                                                     'best_parameter_random_forest  of the BestModel class')
            raise Exception()

    def best_parameter_for_xg(self, train_x, train_y):
        """
        Method Name: get_best_model
        Description: Find out the Model which has the best AUC score.
        Output: The best model name and the model object
        :param train_x:
        :param train_y:
        :return:
        """

        self.logger_object.log(self.file_object, 'Entered the best_parameter_for_xg method of the BestModel class')
        try:
            # initializing with different combination of parameters
            self.grid_param_xg = {

                'learning_rate': [0.5, 0.1, 0.01, 0.001],
                'max_depth': [3, 5, 10, 20],
                'n_estimators': [10, 50, 100, 200]

            }
            # Creating an object of the Grid Search class
            self.grid = GridSearchCV(XGBClassifier(objective='binary:logistic'), self.grid_param_xg, verbose=3, cv=5)
            # finding the best parameters
            self.grid.fit(train_x, train_y)

            # extracting the best parameters
            self.learning_rate = self.grid.best_params_['learning_rate']
            self.max_depth = self.grid.best_params_['max_depth']
            self.n_estimators = self.grid.best_params_['n_estimators']

            # creating a new model with the best parameters
            self.xgb = XGBClassifier(learning_rate=self.learning_rate, max_depth=self.max_depth,
                                     n_estimators=self.n_estimators)
            # training the mew model
            self.xgb.fit(train_x, train_y)
            self.logger_object.log(self.file_object, 'XGBoost best params: ' + str(self.grid.best_params_) +
                                   '. Exited the best_parameter_for_xg method of the BestModel class')
            return self.xgb

        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception occurred in best_parameter_for_xg method of the '
                                                     f'BestModel class. Exception message: {e}')
            self.logger_object.log(self.file_object, 'XGBoost Parameter tuning  failed. Exited the '
                                                     'best_parameter_for_xg method of the BestModel class')
            raise Exception()

    def best_model(self, train_x, train_y, test_x, test_y):

        self.logger_object.log(self.file_object, 'Entered the best_model method of the BestModel class')

        # create best model for XGBoost
        try:
            self.xg_boost = self.best_parameter_for_xg(train_x, train_y)
            self.prediction_xgboost = self.xg_boost.predict(test_x)  # Predictions using the XGBoost Model

            # if there is only one label in y, then roc_auc_score returns error. We will use accuracy in that case
            if len(test_y.unique()) == 1:
                self.xgboost_score = accuracy_score(test_y, self.prediction_xgboost)
                self.logger_object.log(self.file_object, f'Accuracy for XGBoost: {self.xgboost_score}')  # Log AUC
            else:
                self.xgboost_score = roc_auc_score(test_y, self.prediction_xgboost)  # AUC for XGBoost
                self.logger_object.log(self.file_object, f'AUC for XGBoost: {self.xgboost_score}')  # Log AUC

            # create best model for Random Forest
            self.random_forest=self.best_parameter_random_forest(train_x, train_y)

            # prediction using the Random Forest Algorithm
            self.prediction_random_forest=self.random_forest.predict(test_x)

            # if there is only one label in y, then roc_auc_score returns error. We will use accuracy in that case
            if len(test_y.unique()) == 1:
                self.random_forest_score = accuracy_score(test_y, self.prediction_random_forest)
                self.logger_object.log(self.file_object, 'Accuracy for RF:' + str(self.random_forest_score))
            else:
                self.random_forest_score = roc_auc_score(test_y, self.prediction_random_forest)  # AUC for Random Forest
                self.logger_object.log(self.file_object, f'AUC for RF: {self.random_forest_score}')

            # comparing the two models
            if self.random_forest_score < self.xgboost_score:
                return 'XGBoost', self.xg_boost
            else:
                return 'RandomForest', self.random_forest

        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception occurred in best_model method of the '
                                                     f'BestModel class. Exception message: {e}')
            self.logger_object.log(self.file_object,
                                   'Model Selection Failed. Exited the best_model method of the BestModel class')
            raise Exception()



