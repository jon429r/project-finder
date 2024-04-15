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
    'INFO': Fore.YELLOW,
}


# Set up a custom color formatter

class ColoredFormatter(logging.Formatter):
    """Class to color logs."""

    def format(self, record):
        """Checks to see if Log is sucessful color it green.

        if not it uses the defined color."""
        levelname = record.levelname
        message = super().format(record)
        color = Fore.GREEN if levelname == 'SUCCESS' else COLOR_CODES.get(levelname, Fore.WHITE)
        return f"{color}{message}{Style.RESET_ALL}"


# Set up logger
root_logger = logging.getLogger()
for handler in root_logger.handlers:
    handler.setFormatter(ColoredFormatter('%(asctime)s - %(levelname)s - %(message)s'))


class Logger:
    """Logging class, decorate a function with log_action"""

    @staticmethod
    def log_action(action, severity=logging.INFO):
        """
        Decorator function to log actions performed by methods.

        :param action: Description of the action being performed.
        :param severity: Severity level for logging (default is INFO).
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                try:
                    result = func(*args, **kwargs)
                    message = f"SUCCESS - {action} - {func.__name__}"
                    logging.info(message)
                except Exception as e:
                    levelname = 'FAILURE'
                    message = f"FAILURE - Error in {func.__name__}: {e}"
                    logging.error(message)
                    raise
            return wrapper
        return decorator
