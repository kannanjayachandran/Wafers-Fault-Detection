<div align="center">

## Wafer Fault Detection

## _CODING DOCUMENTATION_

</div>
  
This is an end to end machine learning solution to find faulty wafers from sensor data. The sensor data obtained from wafer manufacturers is used to train a machine learning model. The model is then used to predict faulty wafers. The model is deployed on a web application using Flask. The web application is then deployed on a cloud platform. The model is monitored and retrained using a CI/CD pipeline. My aim is to make this project as production ready as it could be.

### Overview

**The overall solution is divided into 8 parts:**

| Part | Description |
| :--- | :--- |
| 1. Data Ingestion | Ingestion of data from the fixed location and storing it in a database. |
| 2. Data Preprocessing | Preprocessing of the data to make it suitable for training the model. |
| 3. Model Selection | Selection of the best model for the given data. |
| 4. Model Building and Tuning | Building and tuning the model to get the best possible accuracy. |
| 5. Prediction and Model Evaluation | Prediction of the faulty wafers and evaluation of the model. |
| 6. Logging Framework | Logging of the application running process. |
| 7. Model Deployment | Deployment of the model on a web application using Flask. |
| 8. Model Monitoring and Retraining | Monitoring of the model and retraining it using a CI/CD pipeline. |
---

**Each module contains a separate readme file which contains a detailed description of the module.**
