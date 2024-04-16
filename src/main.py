"""This module is used as an entry for the project."""

import sqlite3
from sys import argv
import sys

import tabulate
from colorama import Fore
import configparser as config
import datetime
import logging

from commands import OpenProject, FinishProject, NewProject, LogProject
import auth
from auth import signup
import os
from Logger import Logger


def startup():
    """Startup function prints out the logo when project starts."""
    print('''
           **********   *******   *******     *******    |
          /////**///   **/////** /**////**   **/////**   |   TODO APP
              /**     **     //**/**    /** **     //**  |
              /**    /**      /**/**    /**/**      /**  |   Version 1.0
              /**    /**      /**/**    /**/**      /**  |
              /**    //**     ** /**    ** //**     **   |   Help or ? for help
              /**     //*******  /*******   //*******    |
              //       ///////   ///////     ///////     |
          ''')


startup()

print('Welcome to the project manager!')

config_parser = config.ConfigParser()

# Get the directory of the current script
script_dir = os.path.dirname(os.path.realpath(__file__))
# Construct the relative path to user.ini
config_file_path = os.path.join(script_dir, '../config/user.ini')

config_parser.read(config_file_path)

SIGNUP = False

# Sign up if the user needs to sign up
if config_parser.get('LastLogin', 'last_login') == '0000-00-00 00:00:00':
    SIGNUP = True
else:
    SIGNUP = False

if SIGNUP:
    signup.signup_main()

last_login_str = config_parser['LastLogin']['last_login']

# Attempt to parse last_login_str as a datetime object
try:
    last_login = datetime.datetime.strptime(last_login_str, "%Y-%m-%d %H:%M:%S")
except ValueError:
    print("Error: Invalid last login datetime format")
    last_login = None

if last_login is not None:
    current_time = datetime.datetime.now()
    time_difference = current_time - last_login
    if time_difference.days > 1:
        auth.login()
    else:
        auth.login_pin()
else:
    # Handle the case where last_login_str is not a valid datetime string
    # For example, you might want to log an error or prompt the user to re-enter their login information
    print("Error: Last login datetime is not valid")
    # You can add additional logic here as needed


# take in data from the user and pass it to the database
connection = sqlite3.connect(database='database.db')
cursor = connection.cursor()


@Logger.log_action(action='Run todo command', severity=logging.INFO)
def todo_command():
    """This function commands shows user all current projects when called."""
    print('Viewing existing projects...')
    try:
        cursor.execute('SELECT * FROM projects')
        projects = cursor.fetchall()
        tb_headers = ['ID', 'Name', 'Directory', 'link']
        print(tabulate.tabulate(projects, headers=tb_headers, tablefmt='grid'))
        print('... done!')
    except 'NoProjectsFound':
        print('No projects found, please create a new project.')
    sys.exit()


@Logger.log_action(action='Run main.py #main# command', severity=logging.INFO)
def main():
    """This is the main function which is called by the TODO.sh script.

    called by todo.sh script
    """

    full_command = ' '.join(argv[1:])

    exit = False
    while not exit:
        user_input = Fore.RED + ''.join('Todo: ' + full_command) + Fore.RESET
        print(user_input)

        match argv[1]:
            case 'help' | '?':
                if '-v' in argv:
                    help_command_verbose()
                else:
                    help_command()
                LogProject.log_command(full_command, True)
                sys.exit()
            case 'new':
                new_project_instance = NewProject()
                new_project_instance.new_project()
                #NewProject.new_project()
                #LogProject.log_command(full_command, True)
                sys.exit()
            case 'todo':
                todo_command()
                #LogProject.log_command(full_command, True)
                sys.exit()
            case 'finish':
                FinishProject.FinishedProject()
                #LogProject.log_command(full_command, True)
                sys.exit()
            case 'open':
                open_project_instance = OpenProject()
                open_project_instance.open_project()
                #LogProject.log_command(full_command, True)
                sys.exit()
            case 'exit':
                #LogProject.log_command(full_command, True)
                exit = True
            case _:
                print("""Invalid command, please try again. Type
                       "help" for a list of commands.""")
                #LogProject.log_command(full_command, False)
                sys.exit()
        sys.exit()
    print('Come again!')
    sys.exit()


main()
