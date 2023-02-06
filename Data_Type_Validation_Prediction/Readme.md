<div align="center">

# Data Type Validation (Prediction)

</div>

### In this folder we are having the following file:

- DataTypeValidationPrediction.py

> The `DataTypeValidationPrediction.py` file contains the code for handling database connection and performing the 
data type validation on the prediction data. `DBOperation` is the name of the class, and it contains the 
following functions.

1. `database_connection()` - This method creates a database with the given name and if the database already exists;
     then it opens a connection to the database.
2. `db_create_table()` - This method creates a table in the database with the given name and if the table already exists;
     then it opens a connection to the table.
3. `insert_into_table_good_data()` - This method inserts the Good data files from prediction in the table.
4. `select_data_from_csv_to_table()` - This method selects the data from the csv file and inserts it into the table.

