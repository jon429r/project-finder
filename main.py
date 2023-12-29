'''
    can open safari using the command: os.system('open -a Safari')
    use this to implement the open command for internet links
    maybe include a column in the table to include links to project websites
    aka projects that don't have physical directories on the local computer

    can also open vs code with the command: os.system('open -a "Visual\ Studio\ Code')

    use validators library to check urls before opening

    In the open_command function, you are trying to get the project_id using project_id
    = cursor.execute('SELECT id FROM projects WHERE name=?', project_name). Instead, use
    fetchone() to retrieve the result and then get the id. Also, handle cases where the project
    with the given name doesn't exist.

    It's good practice to close the database connection when your script is finished executing.
    You can do this using connection.close().

    You are already using f-strings for string formatting, which is great.
    Continue using them for consistency and improved readability.

    Separation of Concerns:
Consider breaking down your code further into separate modules or classes, each responsible for a specific aspect of the
application (e.g., a module for database operations, a module for project management functions, etc.). This can improve
code organization and maintainability.
Use Functions for Repeated Code:
Identify sections of code that are repeated and consider encapsulating them in functions. For example, the code that
handles confirming user actions and the code that opens projects in Safari or Finder could be extracted into functions.
Consistent Naming Conventions:
Ensure consistent naming conventions for variables, functions, and comments. This improves readability and
maintainability. For example, use consistent casing (e.g., snake_case for variables and functions, CamelCase for classes).
Error Handling:
Enhance error handling to provide more informative error messages and gracefully handle unexpected situations.
Consider logging errors for debugging purposes.
Command Dispatching:
Instead of using multiple if-elif statements to dispatch commands, consider using a dictionary to map commands to
functions. This can make the code more scalable and easier to maintain.
Configuration Management:
If there are configuration parameters, such as the database name, consider using a configuration file or environment
variables to manage them centrally.
Documentation:
Add more documentation, including docstrings for functions, to describe their purpose, parameters, and return values.
This helps others (and yourself) understand the code.
Refactor Long Functions:
If functions become too long or handle multiple concerns, consider refactoring them into smaller, focused functions.
This improves readability and makes the code more modular.
Use Context Managers:
Use context managers (with statements) for handling resources like database connections. This ensures that resources
are properly managed and released.
User Interface Improvements:
Consider enhancing the user interface by providing more feedback, clearer prompts, and maybe even incorporating a
command-line argument parser for more flexibility.
'''

import sqlite3
import tabulate
import os
from database import database as db
from open_projects import open as open
from new_project import new_project as np
from finish_project import finished_project as fp

print('Welcome to the project manager!')


# take in data from the user and pass it to the database
connection = sqlite3.connect(database='database.db')
cursor = connection.cursor()


def help_command():
    help_message = """
    List of possible commands: \n
    1. Create a new project: new -name <"project_name"> -dir <"working_directory"> \n
    please insert the whole directory path starting with a '/'
    Additional arguments: \n
    -link <"project_link"> \n
    2. View existing projects: todo \n
    3. Finished an existing project: finish -name <project_name> \n
    You can also remove a project by typing finish -id <project_id> \n
    4. Open an existing project: open -name <project_name> \n
    You can also open a project by typing open -id <project_id> \n
    5. Exit \n
    6. Help \n
    """

    print(help_message)

def todo_command():
    print('Viewing existing projects...')
    try:
        cursor.execute('SELECT * FROM projects')
        projects = cursor.fetchall()
        print(tabulate.tabulate(projects, headers=['ID', 'Name', 'Directory', 'link'], tablefmt='grid'))
        print('... done!')
    except:
        print('No projects found, please create a new project.')




def main():
    exit = False
    while exit == False:    

        user_input = input('Enter a command: ')
        

        if user_input.startswith('help') or user_input == '?':
            help_command()

        elif user_input.startswith('new'):
            np.command(user_input)

        elif user_input.startswith('todo'):
            todo_command()

        elif user_input.startswith('finish'):
            fp.command(user_input)

        elif user_input.startswith('open'):
            open.command(user_input)

        elif user_input.startswith('exit'):
            exit = True
        else:
            print('Invalid command, please try again. Type "help" for a list of commands.')

    print('Come again!')

np = np()
open = open()
fp = fp()

main()
