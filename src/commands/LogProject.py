"""
This module is responsible for logging the commands that are executed by the user
"""

import configparser as config
import datetime
import logging
import os
import sys

from auth import decrypt_data
from Logger import Logger

config_parser = config.ConfigParser()

try:
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.realpath(__file__))
    # Construct the relative path to user.ini
    config_file_path = os.path.join(script_dir, "../../config/user.ini")

    config_parser.read(config_file_path)

    log_file = config_parser.get("Logging", "log_path")

except FileExistsError as e:
    print(f"Error in user.ini file: {e}")
    sys.exit(1)


@Logger.log_action(action="Log command function", severity=logging.ERROR)
def log_command(command, success):  # Corrected `success`
    """
    Function adds to the log file with the information about the current command.

    Args:
        command (str): command with arguments  # Corrected 'arguments'
        success (bool): Indicates whether the command was successful or not
    """
    user = config_parser["User"]["username"]
    decrypted_username = decrypt_data(user)

    if success:  # Corrected `success`
        log_statement = f"{datetime.datetime.now()} {decrypted_username} {command} Success"  # Corrected 'Success'
    else:
        log_statement = f"{datetime.datetime.now()} {decrypted_username} {command} Failure"  # Corrected 'Failure'

    with open(log_file, "a") as file:
        file.write(
            log_statement + "\n"
        )  # Added newline character at the end of log statement
