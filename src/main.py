"""This module is used as an entry for the project."""

import sqlite3
from sys import argv
import sys

import tabulate
from colorama import Fore
import configparser as config
import datetime

from commands import OpenProject, FinishProject, NewProject, LogProject
import auth
from auth import signup
import os


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

if signup:
    signup.signup_main()

# check the last login time and ask for login username and password if it
# has been more than 1 day
# else, ask for the pin

# compare last login time with current time
last_login = config_parser['LastLogin']['last_login']
last_login = datetime.datetime.strptime(last_login, "%Y-%m-%d %H:%M:%S")
current_time = datetime.datetime.now()
time_difference = current_time - last_login
if time_difference.days > 1:
    auth.login()
else:
    auth.login_pin()

# take in data from the user and pass it to the database
connection = sqlite3.connect(database='database.db')
cursor = connection.cursor()


def help_command():
    """Makes a string, called by default and is a less verbose man command."""
    print("""

    list of commands:

    new, todo, finish, open, exit, help

    Short arguments: -n, -d, -l, -c, -i, -v
    long arguments: --name, --dir, --link, --cmd, --id, --verbose

    for a more verbose manual, add -v or --verbose to the help command

    """)


def help_command_verbose():
    """Help command displays all available commands to the user."""
    print("""
        List of available commands and uses:

        1. Create a new project:
        new --name <"proj_name"> --dir <"working_dir> --link <"proj_link">
        new -n <"project_name"> -d <"working_directory"> -l <"project_link">
        Create a new project with a specified name, working dir, and or
        project link.

        2. View existing projects:
        todo --cmd todo
        todo -c todo
        Display a list of existing projects.

        3. Finish an existing project:
        todo --cmd finish --name <project_name> or --id <project_id>
        todo -c finish -n <project_name> or -i <project_id>
        

        4. Open an existing project:
        todo --cmd open --name <project_name>
        Open an existing project by name.
        Alternatively, you can open a project using its ID:
        todo --cmd open --id <project_id>
        todo -c open -n <project_name>
        todo -c open -i <project_id>
        

        5. Exit:
        exit
        Quit the application.

        6. Help:
        todo --cmd help
        todo -c help
        help
        Display this help message.

        Please replace placeholders like <project_name>, <working_directory>,
        <project_link>, and <project_id> with the actual values.
    """)


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


def main():
    """This is the main function which is called by the TODO.sh script.

    called by todo.sh script
    """
    startup()

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
                NewProject.new_project()
                LogProject.log_command(full_command, True)
                sys.exit()
            case 'todo':
                todo_command()
                LogProject.log_command(full_command, True)
                sys.exit()
            case 'finish':
                FinishProject.finish_project()
                LogProject.log_command(full_command, True)
                sys.exit()
            case 'open':
                OpenProject.open_project()
                LogProject.log_command(full_command, True)
                sys.exit()
            case 'exit':
                LogProject.log_command(full_command, True)
                exit = True
            case _:
                print("""Invalid command, please try again. Type
                       "help" for a list of commands.""")
                LogProject.log_command(full_command, False)
                sys.exit()
        sys.exit()
    print('Come again!')
    sys.exit()


main()
