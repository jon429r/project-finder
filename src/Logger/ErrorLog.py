"""
This module provides several logging functions for this project
It includes a log for the following error severity aka log levels
DEBUG
INFO
WARNING
ERROR
CRITICAL
This will come in the form of decorators for functions to be called all around
the project
"""

import logging

logging.basicConfig(level=logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

class Logger:
    @staticmethod
    def log_action(action, severity=logging.INFO):
        """
        Decorator function to log actions performed by methods.

        :param action: Description of the action being performed.
        :param severity: Severity level for logging (default is INFO).
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                logging.log(severity, f"Success - {action} - {func.__name__}")
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logging.error(f"Failure - Error in {func.__name__}: {e}")
            return wrapper
        return decorator


root_logger = logging.getLogger()
for handler in root_logger.handlers:
    handler.setFormatter(formatter)


@Logger.log_action("performing calculations")
def calculate(x, y):
    """Here's your docstring"""
    try:
        result = x / y
        return result
    except Exception as e:
        logging.error(f"Error in calculate: {e}")
        return None


calculate(1, 2)
calculate('dfas', 2)
