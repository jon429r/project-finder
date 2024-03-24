

import sqlite3
from sys import argv
import sys

import tabulate
from open_project import open as open
from new_project import new_project as np
from finish_project import finished_project as fp
from colorama import Fore

print('Welcome to the project manager!')


# take in data from the user and pass it to the database
connection = sqlite3.connect(database='database.db')
cursor = connection.cursor()


def help_command():
    print("""
        List of available commands:

        1. Create a new project:
        new -name <"project_name"> -dir <"working_directory"> -link <"project_link">
        Create a new project with a specified name, working directory, and optional project link.

        2. View existing projects:
        todo
        Display a list of existing projects.

        3. Finish an existing project:
        finish -name <project_name>
        Mark an existing project as finished. You can also remove a project using its ID:
        finish -id <project_id>

        4. Open an existing project:
        open -name <project_name>
        Open an existing project by name. Alternatively, you can open a project using its ID:
        open -id <project_id>

        5. Exit:
        exit
        Quit the application.

        6. Help:
        help
        Display this help message.

        Please replace placeholders like <project_name>, <working_directory>, <project_link>, and <project_id> with the actual values.
    """)

def todo_command():
    print('Viewing existing projects...')
    try:
        cursor.execute('SELECT * FROM projects')
        projects = cursor.fetchall()
        print(tabulate.tabulate(projects, headers=['ID', 'Name', 'Directory', 'link'], tablefmt='grid'))
        print('... done!')
    except:
        print('No projects found, please create a new project.')
    sys.exit()

def startup():
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


def main():
    startup()

    full_command = ' '.join(argv[1:])    

    exit = False
    while not exit:
        user_input = Fore.RED + ''.join('Todo: ' + full_command) + Fore.RESET
        print(user_input)

        match argv[1]:
            case 'help' | '?':
                help_command()
                sys.exit()
            case 'new':
                np.command(full_command)
                sys.exit()
            case 'todo':
                todo_command()
                sys.exit()
            case 'finish':
                fp.command(full_command)
                sys.exit()
            case 'open':
                open.command(full_command)
                sys.exit()
            case 'exit':
                exit = True
            case _:
                print('Invalid command, please try again. Type "help" for a list of commands.')
                sys.exit()

    print('Come again!')
    sys.exit()

np = np()
open = open()
fp = fp()

main()
