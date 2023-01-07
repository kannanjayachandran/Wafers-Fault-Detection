# Application Logging

Application logging is a critical part of any application. It allows you to track the flow of your application and debug issues when they arise.

- The class `App_Logger` has a single method called `log`. The `log` method takes two arguments: a `file_object` and a `log_message`.

- The `log` method first gets the current date and time using the `datetime` module. It then formats the date and time as strings and writes them to the file_object along with the log_message, separated by tabs.

The file_object is expected to be a file-like object that supports the write method, such as a file opened in write mode. The log_message is a string containing the message that you want to log.

For example, if you have a file object `f` and you want to log the message "This is a log message", you could do something like this:

```python
logger = app_Logger()
logger.log(f, "This is a log message")
```

This would write a line to the file in the following format: ``date/time log message``.

- The [test file](./test_app_logger.py) file contains a test for the `App_Logger` class.

**We can run the test file using the following command:**

```bash

python -m unittest test_app_logger.py
```

**Use this logger in asynchronous manner (async io)**
