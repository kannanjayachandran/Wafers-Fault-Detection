<div align="center">

### Application Logging

</div>

Application logging is a critical part of any application. It allows you to track the flow of your application and debug issues when they arise. **Here I am using a custom logging function to log the messages. Python has a built-in logging module; that could also be used**.

- The class `AppLog` has a single method called `app_logger`. The `app_logger` method takes two arguments: a `file_obj` and a `log_message`.

- The `app_logger` method first gets the current date and time using the `datetime` module. It then formats the date and time as strings and writes them to the file_object along with the log_message, separated by tabs.

> The file_object is expected to be a file-like object that supports the write method, such as a file opened in write mode. The log_message is a string containing the message that you want to log.

> The [test file](./test_app_logger.py) file contains a simple test for the `App_Logger` class. Apparently, there is no need of this test file nor this test file is required to run this application. I have wrote this test file just to show how to write a test and it is always a good practice to write a test for your code.

**We can run the test file using the following command:**

```bash

python -m unittest test_app_logger.py
```
