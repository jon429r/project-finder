import sqlite3
import tabulate

##take in data from the user and pass it to the database
connection = sqlite3.connect('database.db')
cursor = connection.cursor()


print('Welcome to the project manager!')
exit = False
while exit == False:    

    print('Please select an option:')
    print('1. Create a new project: new -name <"project_name"> -dir <"working_directory">')
    print('2. View existing projects: todo')
    print('3. Finished an existing project: finish -name <project_name>')
    print('3. Exit')

    user_input = input('Enter a command: ')

    if user_input.startswith('new'):
        print('Creating a new project...')
        cursor.execute('CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY, name TEXT, directory TEXT)')
        parsed_input = user_input.split(' ')
        project_name = parsed_input[2]
        working_directory = parsed_input[4]
        print('... done!')
        print(f'Project name: {project_name}')
        print(f'Working directory: {working_directory}')
        print('Please confirm the details above are correct.')
        confirm = False;
        while confirm == False:
            confirm = input('Y/N')

            if confirm == 'Y':
                print('Adding project to database...')
                cursor.execute('INSERT INTO projects (name, directory) VALUES (?, ?)', (project_name, working_directory))
                connection.commit()
                print('... done!')
                confirm = True
            elif confirm == 'N':
                print('Canceling project creation...')
                print('... Canceled!')
                confirm = True
            else:
                print('Invalid input, please try again.')

    if user_input.startswith('todo'):
        print('Viewing existing projects...')
        ##display table of projects using tabulate
        cursor.execute('SELECT * FROM projects')
        results = cursor.fetchall()
        print(tabulate.tabulate(results, headers=['id', 'Project', 'Directory'], tablefmt='grid'))

    if user_input.startswith('finish'):
        parsed_input = user_input.split(' ')
        project_name = parsed_input[2]
        print('Finishing project...')
        print(f'Project name: {project_name}')
        print('Please confirm the details above are correct.')
        confirm = False;
        while confirm == False:
            confirm = input('Y/N')

            if confirm == 'Y':
                print('Removing project from database...')
                cursor.execute('DELETE FROM projects WHERE name = ?', (project_name,))
                cursor.commit()
                print('... done!')
                confirm = True
            elif confirm == 'N':
                print('Canceling project deletion...')
                print('... Canceled!')
                confirm = True
            else:
                print('Invalid input, please try again.')

    if user_input.startswith('exit'):
        print('Exiting...')
        exit = True

print('Come again!')