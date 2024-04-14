"""
This module is used to setup the user.ini file for the user. It will ask the
 user for a username, password, email, default code editor, default browser, 
 and setup the default database and logging paths. It will also generate a key 
 for encryption and store it in the user.ini file.
"""

import configparser as config
import os
import sys
import getpass
from cryptography.fernet import Fernet
import datetime
import logging

from auth.login import log_signin
from Logger import Logger

config = config.ConfigParser()

# Get the directory of the current script
script_dir = os.path.dirname(os.path.realpath(__file__))
PATH = script_dir
# Construct the relative path to user.ini
config_file_path = os.path.join(script_dir, "../../config/user.ini")
config.read(config_file_path)


@Logger.log_action(action='Encypting data', severity=logging.ERROR)
def encrypt_data(data, key):
    """
    Encrypt the data using Fernet
    """
    cipher_suite = Fernet(key)
    return cipher_suite.encrypt(data.encode()).decode()


@Logger.log_action(action='Signing up new user', severity=logging.INFO)
def user_signup():
    """
    Ask the user for a username, password, and email
    """
    username = input("Enter a username: ")

    confirm = False
    while confirm is False:
        password = getpass.getpass("Enter a password: ")
        confirm_password = getpass.getpass("Please Confirm the Password: ")

        if password == confirm_password:
            confirm = True
        else:
            continue

    email = input("Enter your email: ")

    confirm = False
    while confirm is False:
        pin = getpass.getpass("Enter a pin, must be at least 4 digits: ")
        confirm_pin = getpass.getpass("Please confirm your pin: ")

        if pin == confirm_pin and len(pin) >= 4:
            confirm = True
        else:
            continue

    last_login = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    key = Fernet.generate_key().decode()

    # Encrypt the username, password, and email
    username = username, key
    password = encrypt_data(password, key)
    email = encrypt_data(email, key)
    pin = encrypt_data(pin, key)

    # Write to user.ini file
    config["User"] = {
        "username": username,
        "password": password,
        "email": email,
        "pin": pin,
    }
    config["LastLogin"] = {"last_login": last_login}

    return key


@Logger.log_action(action='Obtaining User defaults', severity=logging.INFO)
def user_defaults():
    """
    Ask the user for the default code editor and default browser
    """
    code_editor = input("Enter your default code editor: ")
    browser = input("Enter your default browser: ")

    # Write to user.ini file
    config["UserDefaults"] = {"code_editor": code_editor, "browser": browser}


@Logger.log_action(action='Setting up Database path', severity=logging.CRITICAL)
def database_default():
    """
    Setup the default database path
    """
    db_path = os.path.join(PATH, "database.db")

    # Write to user.ini file
    config["Data"] = {"path": db_path}


@Logger.log_action(action='Setting up Logging path', severity=logging.CRITICAL)
def logging_default():
    """
    Setup the default log file path
    """
    log_path = os.path.join(PATH, "logs", "todo.log")

    # Write to user.ini file
    config["Logging"] = {"log_path": log_path}


@Logger.log_action(action='Signing up for new user #MAIN#', severity=logging.CRITICAL)
def signup_main():
    """
    Main function that calls all the other functions
    """

    # Setup parser
    try:
        config.read(config_file_path)
    except FileNotFoundError:
        print("Error reading user.ini file")
        sys.exit(1)

    print("Welcome to my todo app!")
    print("Let's get you signed up so you can be more productive!")

    key = user_signup()
    user_defaults()
    # Store key

    config["Key"] = {"key": key}

    print("That's all we need from you, let us setup the rest for you!")

    database_default()
    logging_default()

    # Write configuration to file
    with open(config_file_path, "w") as config_file:
        config.write(config_file)

    log_signin(True)

    print("You are all set up! Enjoy the app!")


@Logger.log_action(action='getting security key', severity=logging.ERROR)
def get_key():
    """
    Returns key from the config file
    """
    return config.get("Key", "key")
