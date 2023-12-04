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

def new_command(user_input):
    print('Creating a new project...')
    cursor.execute('CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY, name TEXT, directory TEXT, link TEXT)')
    parsed_input = user_input.split(' ')
    project_name = parsed_input[2]
    if parsed_input[3] == '-dir':
        working_directory = parsed_input[4]
    elif parsed_input[3] == '-link' and len(parsed_input) <= 4:
        project_link = parsed_input[4]
        working_directory = 'None'
    if len(parsed_input) >= 5:
        if parsed_input[5] == '-dir':
            working_directory = parsed_input[6]
        elif parsed_input[5] == '-link':
            project_link = parsed_input[6]
    try:
        print(f'Project name: {project_name}')
    except:
        print(f'Project name: None')
    try:
        print(f'Working directory: {working_directory}')
    except:
        print('Working directory: None')
    try:
        print(f'Project link: {project_link}')
    except:
        print('Project link: None')

    print('Please confirm the details above are correct.')
    confirm = False;
    while confirm == False:
        confirm = input('Y/N')

        if confirm == 'Y':
            print('Adding project to database...')
            try:
                # Create finished_projects table if it doesn't exist
                cursor.execute('CREATE TABLE IF NOT EXISTS finished_projects \
                (id INTEGER PRIMARY KEY, name TEXT, directory TEXT, link TEXT)')
                cursor.execute('INSERT INTO projects (name, directory, link) VALUES (?, ?, ?)'
                               , (project_name, working_directory, project_link))
                cursor.execute('DELETE FROM projects WHERE name = ?', (project_name,))

                connection.commit()
            except:
                print('Error: Unable to add project to database.')
                return
            print('... done!')
            confirm = True
        elif confirm == 'N':
            print('Canceling project creation...')
            print('... Canceled!')
            confirm = True
        else:
            print('Invalid input, please try again.')

def todo_command():
    print('Viewing existing projects...')
    try:
        cursor.execute('SELECT * FROM projects')
        projects = cursor.fetchall()
        print(tabulate.tabulate(projects, headers=['ID', 'Name', 'Directory', 'link'], tablefmt='grid'))
        print('... done!')
    except:
        print('No projects found, please create a new project.')

def finish_command(user_input):
    print('Finishing project...')
    parsed_input = user_input.split(' ')
    if parsed_input[1] == '-id':
        project_id = parsed_input[2]
        print(f'Project ID: {project_id}')
        print('Please confirm the details above are correct.')
        confirm = False
        while not confirm:
            confirm = input('Y/N')

            if confirm == 'Y':
                print('Removing project from database...')
                # Create finished_projects table if it doesn't exist
                cursor.execute('CREATE TABLE IF NOT EXISTS finished_projects '
                               '(id INTEGER PRIMARY KEY, name TEXT, directory TEXT, link TEXT)')
                # Move the project to the finished projects table
                cursor.execute('INSERT INTO finished_projects (name, directory, link) '
                               'SELECT name, directory, link FROM projects WHERE id = ?', (project_id,))
                cursor.execute('DELETE FROM projects WHERE id = ?', (project_id,))
                connection.commit()
                print('... done!')
            elif confirm == 'N':
                print('Canceling project deletion...')
                print('... Canceled!')
            else:
                print('Invalid input, please try again.')

    elif parsed_input[1] == '-name':
        project_name = parsed_input[2]
        print(f'Project name: {project_name}')
        print('Please confirm the details above are correct.')
        confirm = False
        while not confirm:
            confirm = input('Y/N')

            if confirm == 'Y':
                print('Removing project from database...')
                # Create finished_projects table if it doesn't exist
                cursor.execute('CREATE TABLE IF NOT EXISTS finished_projects (id INTEGER PRIMARY KEY, name TEXT, directory TEXT, link TEXT)')
                # Move the project to the finished projects table
                cursor.execute('INSERT INTO finished_projects (name, directory, link) SELECT name, directory, link FROM projects WHERE name = ?', (project_name,))
                cursor.execute('DELETE FROM projects WHERE name = ?', (project_name,))
                connection.commit()
                print('... done!')
            elif confirm == 'N':
                print('Canceling project deletion...')
                print('... Canceled!')
            else:
                print('Invalid input, please try again.')


def open_in_safari(project_id):
    cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
    project = cursor.fetchone()
    print(f'Opening project {project[1]}...')
    print(f'Working directory: {project[2]}')
    print(f'Project link: {project[3]}')
    try:
        os.system(f'cd')
        os.system(f'open -a Safari {project[3]}')
    except:
        print('Error: Unable to open project link.')
        input = input('Would you like to manually type in the link: Y/N')
        if input == 'Y' or 'y':
            link = input('What is the link')
            os.system(f'cd')
            os.system(f'open -a Safari {link}')
            return
        elif input == 'N' or 'n':
            print('Cancelling')
        return
    
    print('... done!')

def open_in_finder(project_id):
    cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
    project = cursor.fetchone()
    print(f'Opening project {project[1]}...')
    print(f'Working directory: {project[2]}')
    print(f'Project link: {project[3]}')
    os.system(f'cd')
    try:
        os.system(f'open {project[2]}')
    except:
        print('Error: Unable to open project dir.')
        return

    print('done...!')

def open_command(user_input):
    ##user can open a project using id or name
    print('Opening project...')
    parsed_input = user_input.split(' ')
    if parsed_input[1] == '-id':
        project_id = parsed_input[2]
        print(f'Project ID: {project_id}')
        print('Please confirm the details above are correct.')
        confirm, deny = False, False
        while confirm or deny is False:
            confirm = input('Y/N')

            if confirm == 'Y':
                choice = False
                while choice is False:
                    print('Where would you like to open the project?')
                    print('1. Finder')
                    print('2. Safari')
                    open_location = -1
                    open_location = input('Enter a number: ')
                    if open_location == '1':
                        open_in_finder(project_id)
                    elif open_location == '2':
                        open_in_safari(project_id)
                    else:
                        print('Invalid input, please try again.')     

                confirm = True

            elif confirm == 'N':
                print('Canceling project opening...')
                print('... Canceled!')
                deny = True
            else:
                print('Invalid input, please try again.')

    elif parsed_input[1] == '-name':
        project_name = parsed_input[2]
        project_id = cursor.execute('SELECT id FROM projects WHERE name=?', project_name)
        print(f'Project name: {project_name}')
        print('Please confirm the details above are correct.')
        confirm = False;
        while confirm == False:
            confirm = input('Y/N')

            if confirm == 'Y':
                choice = False
                while choice is False:
                    print('Where would you like to open the project?')
                    print('1. Finder')
                    print('2. Safari')
                    open_location = -1
                    open_location = input('Enter a number: ')
                    if open_location == '1':
                        open_in_finder(project_id)
                    elif open_location == '2':
                        open_in_safari(project_id)
                    else:
                        print('Invalid input, please try again.')  

            elif confirm == 'N':
                print('Canceling project opening...')
                print('... Canceled!')
                confirm = True
            else:
                print('Invalid input, please try again.')

def main():
    exit = False
    while exit == False:    

        user_input = input('Enter a command: ')

        if user_input.startswith('help') or user_input == '?':
            help_command()

        elif user_input.startswith('new'):
            new_command(user_input)

        elif user_input.startswith('todo'):
            todo_command()

        elif user_input.startswith('finish'):
            finish_command(user_input)

        elif user_input.startswith('open'):
            open_command(user_input)
        elif user_input.startswith('exit'):
            exit = True
        else:
            print('Invalid command, please try again. Type "help" for a list of commands.')

    print('Come again!')

main()
