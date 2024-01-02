import sqlite3

class new_project:
    def __init__(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()

    def command(self, user_input):
        from database import database as dataclass
        db = dataclass()
        print('Creating a new project...')
        try:
            db.create_table(table_name='projects')
        except TypeError as e:
            print(f'Error: Unable to create table. {e}')
            return
        parsed_input = user_input.split(' ')
        project_name = None
        project_link = None
        working_directory = None

        if len(parsed_input) == 3:
            project_name = parsed_input[2]

        if len(parsed_input) == 4:
            if parsed_input[3] == '-dir' and len(parsed_input) >= 5:
                working_directory = parsed_input[4]
            elif parsed_input[3] == '-link' and len(parsed_input) == 5:
                project_link = parsed_input[4]
                working_directory = 'None'

        if len(parsed_input) == 7:
            if parsed_input[5] == '-dir' and len(parsed_input) == 7:
                working_directory = parsed_input[6]
            elif parsed_input[5] == '-link' and len(parsed_input) == 7:
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
                    db.create_table('projects')
                    db.new_project(name=project_name, directory=working_directory, link=project_link)
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

