## Data Ingestion

Data Ingestion is the process of obtaining or extracting data from a source and loading it into a data warehouse. Data ingestion is the first step in the data pipeline. In this module we have:

1. [data_loader_training.py](./data_loader.py)

- **data_loader_training.py** : This file contains the class and methods used to get data from the source for training. The class is called `DataGetterTraining` and it contains the following method:

- `get_data(self)` - This method is used to get the data from the source and load it into a pandas dataframe.
