import sqlite3
from sys import argv
import sys

class new_project:
    def __init__(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        
    def command(self, cmd):
        from database import database as dataclass
        db = dataclass()
        print('Creating a new project...')
        try:
            db.create_table(table_name='projects')
        except TypeError as e:
            print(f'Error: Unable to create table. {e}')
            return 400

        project_name, working_directory, project_link = argv[2], argv[3], argv[4]
     
        if project_name == None:
            print('Error: Please specify a project name.')
            return

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
            confirmation = input('Y/N')

            if confirmation == 'Y':
                print('Adding project to database...')
                try:
                    # Create finished_projects table if it doesn't exist
                    db.create_table('projects')
                    db.new_project(name=project_name, directory=working_directory, link=project_link)
                except:
                    print('Error: Unable to add project to database.')
                    return 400
                print('... done!')
                confirm = True
            elif confirm == 'N':
                print('Canceling project creation...')
                print('... Canceled!')
                confirm = True
            else:
                print('Invalid input, please try again.')
        sys.exit()


