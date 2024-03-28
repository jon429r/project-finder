"""
This file is responsible for opening a project in the user's preferred editor.
"""

import sqlite3
import os
import sys
from sys import argv

from database import Database as dataclass

class OpenProject:
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
        if isinstance(argv[2], int):
            project_id = argv[2]
            print(f'Project ID: {project_id}')
        else:
            project_name = argv[2]
            self.cursor.execute('SELECT id FROM projects WHERE name=?', (project_name,))
            project_id = self.cursor.fetchone()[0]
            print(f'Project ID: {project_id}')


        project_info = self.db.get_project_info('id', project_id)
        # check to make sure the return is not none
        if project_info is None:
            print('Error: Project not found.\n Now exiting...')
            sys.exit()

        print(f'Project Info: {project_info}')
        print('Please confirm the details above are correct.')
        confirm = False
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

                    #case match statement to open project in specified location
                    try:
                        match open_location:
                            case '1':
                                self.in_finder('id', project_id)
                            case '2':
                                self.in_safari('id', project_id)
                            case '3':
                                self.in_code_editor('id', project_id)
                            case 'q':
                                print('Canceling operation, closing now...')
                                sys.exit()
                    except ValueError as e:
                        print(f'Invalid input, please try again: {e}')

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
        if isinstance(argv[2], int):
            project_id = argv[2]
            print(f'Project ID: {project_id}')
        else:
            project_name = argv[2]
            self.cursor.execute('SELECT id FROM projects WHERE name=?', (project_name,))
            project_id = self.cursor.fetchone()[0]
            print(f'Project ID: {project_id}')

        try:
            #get project info from database
            project = self.db.get_project_info('id', project_id)

            if project:
                print(f'Opening project {project[1]}...')
                print(f'Working directory: {project[2]}')
                print(f'Project link: {project[3]}')
                project_link = project[3]

                print('Opening {project_link} in Safari...')
                os.system(f'open -a Safari {project_link}')
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

        
        working_dir = project[2]
        if working_dir.startswith('/'):
            working_dir = working_dir.join('~')
        else:
            working_dir = working_dir.join('~/')

        print(f'Opening {working_dir} in Finder...')
        try: 
            os.system(f'open {working_dir}')
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
               project = self.db.get_project_info(identifier, argv[2])
        except:
            print('Error: Finding project in database.')
        print(f'Opening project {project[1]}...')
        print(f'Working directory: {project[2]}')
        print(f'Project link: {project[3]}')

        os.system(f'cd')
        print(f'Opening {project[2]} in default code editor...')
        try:
            dir = '~/' + project[2]
            print(f'dir: {project[2]}')
            os.system(f'nvim {project[2]}')
        except:
            print('Error: Unable to open project in neovim.')
            return 400
        sys.exit()
