import sqlite3

class finished_project:
    def __init__(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()

    def command(self, user_input):
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
                    from database import database as dataclass
                    db = dataclass()
                    db.remove_project_id(project_id)

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
                    db.remove_project_name(project_name)

                elif confirm == 'N':
                    print('Canceling project deletion...')
                    print('... Canceled!')
                else:
                    print('Invalid input, please try again.')
