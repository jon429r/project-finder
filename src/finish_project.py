"""
Module defines several functions for the finish command
"""

import sqlite3
import sys
from sys import argv

from database import database as dataclass

class finished_project:
    """
    class hosts multiple functions for finish command
    """
    def __init__(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self.db = dataclass()


    def command(self, user_input):
        """
        command function

        @args -- user_input

        """
        print('Finishing project...')
        parsed_input = user_input.split(' ')
        if parsed_input[1] == '-id':
            project_id = parsed_input[2]
            project_info = self.db.get_project_info('id', project_id)
            if project_info is not None:
                info = f"ID: {project_info[0]} \nName: {project_info[1]} \nDirectory: {project_info[2]} \nLink: {project_info[3]}"
                print(info)
            else:
                print("Project not found.")

            print('Please confirm the details above are correct.')
            confirm = False
            while not confirm:
                confirm = input('Y/N')

                if confirm == 'Y':
                    db = dataclass()
                    db.remove_project('id', project_id)

                elif confirm == 'N':
                    print('Canceling project deletion...')
                    print('... Canceled!')
                else:
                    print('Invalid input, please try again.')

        project_name = argv[2]
        project_info = self.db.get_project_info('name', project_name)
        if project_info is not None:
            info = f"ID: {project_info[0]}, Name: {project_info[1]}, Directory: {project_info[2]}, Link: {project_info[3]}"
            print(info)
        else:
            print("Project not found.")

        print('Please confirm the details above are correct.')
        confirm = False
        while not confirm:
            confirm = input('Y/N')

            if confirm == 'Y':
                self.db.remove_project('name', project_name)
            elif confirm == 'N':
                print('Canceling project deletion...')
                print('... Canceled!')
            else:
                print('Invalid input, please try again.')
            sys.exit()
