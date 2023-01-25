<div align="center">

# Wafer Fault Detection

## _CODING DOCUMENTATION_

</div>

> This section contains the step by step process through which I have created this project. It would describe the folder structure, classes inside each folders, and functions inside each classes.  

## Overview

**The overall solution is divided into 8 parts:**

* Data ingestion
* Data Preprocessing
* Model Selection
* Model Building and Tuning
* Prediction and Model Evaluation
* Logging Framework
* Model Deployment
* Model Monitoring
* Model Retraining
* CI/CD

---

## Application Logger

>First we need to Create a Custom Application Logger to log each and every step of the application running process. The inbuilt logging module of python is avoided simply because it not thread safe. This is prerequisite for the project

1. A folder is created with the name `Application_Logging`.
2. Create a file called `application_logger.py` in the `Application_Logging` folder, which contains the `AppLog` class.
3. The `AppLog` class contains the `app_logger method` which is used to create a logger object.

## Data Ingestion

>This is the first step of the project. From here our data pipeline starts. The data is ingested from the fixed location and stored in a database.

1. Create a database schema for training the data [Training Schema](../Training_Schema.json)

``` py
 Database schema is the structure of the database; more like a blueprint of the database. It defines the tables, columns, and relationships between the tables. It also defines the data types of the columns.

```

2. Create a folder called `Prediction_Raw_Data_Validation` in the root directory.
3. Create a file called `DataValidationPrediction` in the `Prediction_Raw_Data_Validation` folder, which contains the `DataValidationPrediction` class.
4. The `DataValidationPrediction` class contains the following functions;

``` python

valuesFromSchema() # This function is used to extract values from the schema file.
RegexCreator() # This function is used to create a regex pattern for the validation of the data.


```
