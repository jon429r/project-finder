"""
This module provides several logging functions for this project.

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
from colorama import Fore, Style

logging.basicConfig(level=logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Define color codes
COLOR_CODES = {
    'ERROR': Fore.RED,
    'CRITICAL': Fore.RED,
    'WARNING': Fore.YELLOW,
    'INFO': Fore.GREEN,
}

# Set up a custom color formatter
class _ColoredFormatter(logging.Formatter):
    """Formats the Color of the log message"""

    def format(self, record):
        """Function that formats the color of the log message"""
        levelname = record.levelname
        message = super().format(record)
        color = COLOR_CODES.get(levelname, Fore.WHITE)
        return f"{color}{message}{Style.RESET_ALL}"

# Set up logger
root_logger = logging.getLogger()
for handler in root_logger.handlers:
    handler.setFormatter(_ColoredFormatter('%(asctime)s - %(levelname)s - %(message)s'))

class Logger:
    """Logging class, decorate a function with log_action"""

    # Initialize logger instance
    logger = logging.getLogger(__name__)

    @staticmethod
    def log_action(action, severity=logging.INFO):
        """
        Decorator function to log actions performed by methods.

        :param action: Description of the action being performed.
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                levelname = None
                message = "Logging Failure??"
                try:
                    result = func(*args, **kwargs)
                    levelname = 'INFO'
                    message = f"SUCCESS - {action} - {func.__name__}"
                    Logger.logger.log(severity, message)  # Use logger instance from Logger class
                    return result
                except TypeError as e:
                    levelname = 'ERROR'
                    message = f"FAILURE - {e}"
                    Logger.logger.log(severity, message)  # Use logger instance from Logger class
                    raise
                except Exception as e:
                    levelname = 'FAILURE'
                    message = f"FAILURE - Error in {func.__name__}: {e}"
                    Logger.logger.log(severity, message)  # Use logger instance from Logger class
                    raise
                finally:
                    pass
                
            return wrapper
        return decorator
