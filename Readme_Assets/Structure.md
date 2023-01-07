# Project Structure

## 1. Application Logger

Created a Custom Application Logger to log each and every step of the application running process.

## 2. Aquired Data

The data is obtained as batches to a fixed location. The data contains the Wafer names and 590 columns of different sensor values for each wafer. The last column will have the "Good/Bad" value for each wafer.

## 3. Data Ingestion

The data is ingested from the fixed location and stored in a database.

1. Created a database schema for the data (prediction schema).
