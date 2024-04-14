"""
Module adds to the log file with the information about the correct command
date, time, user, command, arguments
ex: 2024-04-05 21:41:23 user todo finish --name project_2
"""

import datetime
import sys
import os

import configparser as config

from auth import decrypt_data


config_parser = config.ConfigParser()

try:
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.realpath(__file__))
    # Construct the relative path to user.ini
    config_file_path = os.path.join(script_dir, '../../config/user.ini')

    config_parser.read(config_file_path)

    log_file = config_parser.get('Logging', 'log_path')

except FileExistsError as e:
    print(f"Error in user.ini file: {e}")
    sys.exit(1)


def log_command(command, success):
    """
    Function adds to the log file with the information about the correct command

    Args:
        command (str): command with arguments
    """
    user = config_parser['User']['username']
    decrypted_username = decrypt_data(user)
    if success:
        log_statement = f'{datetime.datetime.now()} {decrypted_username} {command} success'
    else:
        log_statement = f'{datetime.datetime.now()} {decrypted_username} {command} Failure'

    with open(log_file, 'a') as file:
        file.write(log_statement)

def log_signin(success):
    """
    Function adds to the log file with the information about the current sign in attempt
    """
    user = config_parser['User']['username']
    decrypted_username = decrypt_data(user)
    if success:
        log_statement = f'{datetime.datetime.now()} {decrypted_username} Login_attempt success'
    else:
        log_statement = f'{datetime.datetime.now()} {decrypted_username} Login_attempt Failure'

    with open(log_file, 'a') as file:
        file.write(log_statement)
