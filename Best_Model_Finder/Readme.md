## Best Model Finder

For this project we are using two main machine learning algorithms;

- XGBoost Algorithm
- Random Forest Algorithm

**XGBoost Algorithm** or Extreme Gradient Boosting is a machine learning technique that uses an ensemble of decision trees to make predictions. XGBoost is known for its speed and accuracy and has been used to win numerous machine learning competitions which makes it a popular supervised learning algorithm. **`XGBclassifier`** is a wrapper class for the XGBoost library.

**Random Forest Classifier** is a supervised learning algorithm that uses ensemble learning method for classification and regression. It is a type of ensemble learning method, where a group of weak learners come together to form a strong learner. **`RandomForestClassifier`** is a wrapper class for the Random Forest Classifier.

In this module we are finding the **best model** for our dataset using the above two algorithms. We are also finding the **best Hyperparameters** for the best model using **Cross Validation**.

In the `BestModel` class we have the following functions:

1. `find_best_pipeline()` : Finds the best model and the best hyperparameter
2. `train_best_model()` : Trains the best model
3. `evaluate_best_model()` : Evaluates the best model
4. `save_best_model()` : Saves the best model
5. `load_best_model()` : Loads the best model

Here I am using the `pipeline` class from the `sklearn` for chaining **training** and **Standardization** steps. After creating the pipeline, we are performing **Cross validation** on both the pipelines to find the accuracy score and AUC score. The pipeline with the best accuracy score and AUC score is considered as the best model.

Then depending on **best model** we are setting up the **best hyperparameters** for the model. If the pipeline using the Random Forest algorithm is best, then the hyperparameters that will be tuned are `n_estimators` and `max_depth` of the `Random Forest model`. The search space for each hyperparameter is given by the lists `[10, 50, 100]` and `[5, 10, 20]`, respectively. If the pipeline using the XGBoost algorithm is best, then the hyperparameters that will be tuned are `n_estimators` and `max_depth` of the `XGBoost model`. The search space for each hyperparameter is given by the lists `[10, 50, 100]` and `[5, 10, 20]`, respectively.

And finally we would return the `best pipeline` containing the best model and the best hyperparameters.

In the `train_best_model()` function we are training the best model using the `fit()` function on the entire training dataset

In the `evaluate_best_model()` function we are evaluating the best model using the `predict()` function on the entire test dataset

In the `save_best_model()` function we are saving the best model using the `joblib` library

Finally in the `load_best_model()` function we are loading the best model using the `joblib` library
