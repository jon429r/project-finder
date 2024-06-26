"""
this file is used to login to the system from the information in user.ini
"""

import configparser as config
import datetime
import getpass
import logging
import os
import sys

from cryptography.fernet import Fernet

from Logger import Logger

config = config.ConfigParser()

# Get the directory of the current script
script_dir = os.path.dirname(os.path.realpath(__file__))
PATH = script_dir
# Construct the relative path to user.ini
config_file_path = os.path.join(script_dir, "../../config/user.ini")
config.read(config_file_path)

try:
    log_file = config.get("Logging", "log_path")
except KeyError:
    print("Logging: file not found in user.ini file, trying Logging: log_file")
    config["Logging"] = {"file": "file"}


def log_signin(success):
    """
    Function adds to the log file with the information about the current sign in attempt
    """
    # cypher_key = config.get('Key','key').encode()

    decrypted_username = config.get("User", "username")
    if success:
        log_statement = (
            f"{datetime.datetime.now()} {decrypted_username} Login_attempt success\n"
        )
    else:
        log_statement = (
            f"{datetime.datetime.now()} {decrypted_username} Login_attempt Failure\n"
        )

    with open(log_file, "a") as file:
        file.write(log_statement)


@Logger.log_action(action="decypt data", severity=logging.ERROR)
def decrypt_data(data):
    """
    Decrypt the data using Fernet
    """
    from .signup import get_key

    cypher_key = get_key()
    cipher_suite = Fernet(cypher_key)
    return cipher_suite.decrypt(data)


@Logger.log_action(action="load configuration file", severity=logging.CRITICAL)
def load_configuration():
    """
    Load the user configuration from the INI file
    """
    try:
        config.read(config_file_path)
    except FileNotFoundError:
        print("Error reading user.ini file")
        sys.exit(1)


@Logger.log_action(action="logging in w/username+pass", severity=logging.INFO)
def login(username=None, password=None):
    """
    Prompt the user for login credentials and verify them
    """
    load_configuration()
    if username and password is None:
        username = input("Enter your username: ")
        password = getpass.getpass("Enter your password: ")

    stored_username = config["User"].get("username", "")
    stored_password = config["User"].get("password", "")

    stored_password = decrypt_data(stored_password).decode()

    if password == stored_password and username == stored_username:
        print("Login successful!")
        config["LastLogin"] = {
            "last_login": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        log_signin(True)
        return True
    else:
        print("Invalid username or password. Please try again.")
        log_signin(False)
        return False


@Logger.log_action(action="logging in w/pin", severity=logging.INFO)
def login_pin():
    """
    Prompt the user for their pin and verify it
    """

    load_configuration()

    pin = input("Enter your pin: ")

    stored_pin = config["User"].get("pin", "")

    if pin == decrypt_data(stored_pin).decode():
        print("Pin correct!")
        log_signin(True)
    else:
        print("Invalid pin. Please try again.")
        log_signin(False)
        sys.exit(1)
