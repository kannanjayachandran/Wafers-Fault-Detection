<div align="center">
  
# Data Ingestion

</div>

### Data Ingestion is the process of obtaining or extracting data from a source and loading it into a data warehouse. Data ingestion is the first step in the data pipeline. In this folder there are two files

1. data_loader.py
2. data_loader_prediction.py

### data_loader.py

> This file contains the class and methods used to get data from the source for training. The class is called DataGetter and it contains the following method:

- `get_data(self)` - This method is used to get the data from the source and load it into a pandas dataframe.

### data_loader_prediction.py

> This file contains the class and methods used to get data from the source for prediction. The class is called DataGetterPrediction and it contains the following method:

- `get_data_prediction(self)` - This method is used to get the data from the source and load it into a pandas dataframe.
