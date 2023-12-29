import sqlite3
import os

class open:
    def __init__(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()

    def command(self, user_input):
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
                        open_location = input('Enter a number or Q to quit: ')
                        if open_location == '1':
                            self.in_finder('id', project_id)
                        elif open_location == '2':
                            self.in_safari('id', project_id)
                        elif open_location.lower() == 'q':
                            confirm = 'N'
                            break
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
            project_id = self.cursor.execute('SELECT id FROM projects WHERE name=?', (project_name,))
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
                        open_location = input('Enter a number or Q to quit: ')
                        if open_location == '1':
                            self.in_finder('name', project_id)
                        elif open_location == '2':
                            self.in_safari('name', project_id)
                        elif open_location.lower() == 'q':
                            confirm = 'N'
                            break
                        else:
                            print('Invalid input, please try again.')  

                elif confirm == 'N':
                    print('Canceling project opening...')
                    print('... Canceled!')
                    confirm = True
                else:
                    print('Invalid input, please try again.')

    def in_safari(self, identifier, project_id):
        try:
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

    def in_finder(self, identifier, project_id):
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
            return

        print('done...!')

