"""
This file is responsible for opening a project in the user's preferred editor.
"""

import sqlite3
import os
import sys
from sys import argv

from database import Database as dataclass

class Open:
    """
    This class provides the functionality to open a project.
    """
    def __init__(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self.db = dataclass()
    def command(self, user_input):
        """
        command function

        :param user_input: The user input to parse and execute.
        """
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
                        print('3. Code Editor')
                        open_location = -1
                        open_location = input('Enter a number or Q to cancel: ')
                        if open_location == '1':
                            self.in_finder('id', project_id)
                        elif open_location == '2':
                            self.in_safari('id', project_id)
                        elif open_location == '3':
                            self.in_code_editor('id', project_id)
                        elif open_location.lower() == 'q':
                            confirm = 'N'
                            print('Canceling project opening...')
                            return 400
                        else:
                            print('Invalid input, please try again.')

                    confirm = True

                elif confirm == 'N':
                    print('Canceling project opening...')
                    print('... Canceled!')
                    deny = True
                    return 400
                else:
                    print('Invalid input, please try again.')
            sys.exit()

        project_name = argv[2]
        project_id = self.cursor.execute('SELECT id FROM projects WHERE name=?', (project_name,))
        print(f'Project name: {project_name}')
        print('Please confirm the details above are correct.')
        confirm = False;
        while confirm is False:
            confirm = input('Y/N')

            if confirm == 'Y':
                choice = False
                while choice is False:
                    print('Where would you like to open the project?')
                    print('1. Finder')
                    print('2. Safari')
                    print('3. Code Editor')
                    open_location = -1
                    open_location = input('Enter a number or Q to cancel: ')
                    if open_location == '1':
                        self.in_finder('name', project_id)
                    elif open_location == '2':
                        self.in_safari('name', project_id)
                    elif open_location == '3':
                        self.in_code_editor('name', project_id)
                    elif open_location.lower() == 'q':
                        confirm = 'N'
                        print('Canceling project opening...')
                        return 400
                    else:
                        print('Invalid input, please try again.')
            elif confirm == 'N':
                print('Canceling project opening...')
                print('... Canceled!')
                confirm = True
                return 400
            else:
                print('Invalid input, please try again.')
            sys.exit()

    def in_safari(self, identifier, project_id):
        """
        Open the project in Safari.

        :param identifier: The identifier to use to get the project info (e.g. 'id' or 'name').
        :param project_id: The value of the identifier.

        """
        try:
            #get project info from database
            self.cursor.execute(f'SELECT * FROM projects WHERE {identifier} = ?', (project_id,))
            project = self.cursor.fetchone()

            if project:
                print(f'Opening project {project[1]}...')
                print(f'Working directory: {project[2]}')
                print(f'Project link: {project[3]}')

                os.system(f'open -a Safari {project[3]}')
                print('... done!')
            else:
                print('Error: Project not found.')
        except Exception as e:
            print(f'Error: {e}')
            return 400
        sys.exit()

    def in_finder(self, identifier, project_id):
        """
        Open the project in Finder.

        :param identifier: The identifier to use to get the project info (e.g. 'id' or 'name').
        :param project_id: The value of the identifier.

        """
        self.cursor.execute(f'SELECT * FROM projects WHERE {identifier} = ?', (project_id,))
        project = self.cursor.fetchone()
        print(f'Opening project {project[1]}...')
        print(f'Working directory: {project[2]}')
        print(f'Project link: {project[3]}')
        os.system(f'cd')
        try:
            os.system(f'open {project[2]}')
        except:
            print('Error: Unable to open project dir.')
            return 400

        print('done...!')
        sys.exit()

    def in_code_editor(self, identifier, project):
        """
        Open the project in the user's preferred code editor.

        :param identifier: The identifier to use to get the project info (e.g. 'id' or 'name').
        :param project: The value of the identifier.
        """
        try:
               project = self.db.get_project_info("name", argv[2])
        except:
            print('Error: Finding project in database.')
        print(f'Opening project {project[1]}...')
        print(f'Working directory: {project[2]}')
        print(f'Project link: {project[3]}')
        os.system(f'cd')
        try:
            dir = '~/' + project[2]
            print(f'dir: {project[2]}')
            os.system(f'nvim {project[2]}')
        except:
            print('Error: Unable to open project in neovim.')
            return 400
        sys.exit()
