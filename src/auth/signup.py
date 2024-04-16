"""
This module is used to setup the user.ini file for the user.

It will ask the
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

try:
    log_file = config.get('Logging', 'log_path')
except KeyError:
    print("Logging: file not found in user.ini file, trying Logging: log_file")
    config["Logging"] = {"file": 'file'}


@Logger.log_action(action='Update Last login time', severity=logging.ERROR)
def update_last_login():
    # Get current datetime
    new_login_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print('New login time:', new_login_time)

    # Update last login time in configuration
    config.set('LastLogin', 'last_login', new_login_time)

    return new_login_time


@Logger.log_action(action='Encypting data', severity=logging.ERROR)
def encrypt_data(data, key):
    """
    Encrypt the data using Fernet
    """
    if key and data is not None:
        cipher_suite = Fernet(key)
        encrypted_data = cipher_suite.encrypt(data.encode())
        return encrypted_data.decode()
    else:
        print("Error: Key or data is None")
        sys.exit(1)


@Logger.log_action(action='Signing up new user', severity=logging.INFO)
def user_signup(username=None, password=None, email=None, pin=None):
    """
    Ask the user for a username, password, and email
    """
    if username is None or password is None or pin is None or email is None:
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

    key = Fernet.generate_key().decode()

    # Encrypt the username, password, and email
    username = username
    password = encrypt_data(password, key)
    email = encrypt_data(email, key)
    pin = encrypt_data(pin, key)

    # Write to user.ini file
    config["User"] = {
        "username": str(username),
        "password": str(password),
        "email": str(email),
        "pin": str(pin),
    }
    
    time = update_last_login()

    config["LastLogin"] = {"last_login": time}

    with open(config_file_path, "w") as config_file:
        config.write(config_file)

    return key


@Logger.log_action(action='Obtaining User defaults', severity=logging.INFO)
def user_defaults(code_editor=None, browser=None):
    """Ask the user for the default code editor and default browser."""
    if code_editor is None or browser is None:
        code_editor = input("Enter your default code editor: ")
        browser = input("Enter your default browser: ")

    # Write to user.ini file
    config["UserDefaults"] = {"code_editor": str(code_editor), "browser": str(browser)}


@Logger.log_action(action='Setting up Database path', severity=logging.CRITICAL)
def database_default():
    """Setup the default database path."""
    db_path = os.path.join(PATH, "database.db")

    # Write to user.ini file
    config["Data"] = {"path": db_path}


@Logger.log_action(action='Setting up Logging path', severity=logging.CRITICAL)
def logging_default():
    """Setup the default log file path."""
    log_path = os.path.join(PATH, "logs", "todo.log")

    # Write to user.ini file
    try:
        config["Logging"] = {"log_path": log_path}
    except KeyError:
        print("Logging: log_path not found in user.ini file, trying Logging: file")
        config["Logging"] = {"file": log_path}


@Logger.log_action(action='Signing up for new user #MAIN#', severity=logging.CRITICAL)
def signup_main(username=None, password=None, email=None, pin=None, code_editor=None, browser=None):
    """
    Sign up for a new user.
    """
    # Read user.ini file"""
    try:
        config.read(config_file_path)
    except FileNotFoundError:
        print("Error reading user.ini file")
        sys.exit(1)

    print("Welcome to my todo app!")
    print("Let's get you signed up so you can be more productive!")

    if username and password is None:
        key = user_signup()
    else:
        key = user_signup(username, password, email, pin)
    
    if code_editor and browser is None:
        user_defaults()
    else:
        user_defaults(code_editor=code_editor, browser=browser)

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
    try:
        return config.get("Key", "key")
    except KeyError:
        print("Error reading key from user.ini file")
        return None
