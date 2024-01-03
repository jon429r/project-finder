import sqlite3

class database:
    def __init__(self, db_name='database.db'):
        """Initialize the database and create the 'projects' table if it doesn't exist."""
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table('projects')

    def new_project(self, name, directory, link):
        """Add a new project to the 'projects' table."""
        print('Adding project to database...')
        try:
            self.cursor.execute('INSERT INTO projects (name, directory, link) VALUES (?, ?, ?)', (name, directory, link))
            self.connection.commit()
        except sqlite3.IntegrityError as e:
            print(f'Error: Unable to add project to database. {e}')


    def create_table(self, table_name):
        """Create a table if it doesn't exist."""
        try:
            self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} \
                    (id INTEGER PRIMARY KEY, name TEXT, directory TEXT, link TEXT)')
        except sqlite3.OperationalError as e:
            print(f'Error: Unable to create {table_name} table. {e}')


    def remove_project_id(self, id):
        print('Removing project from database...')
        # Create finished_projects table if it doesn't exist
        try:
            self.cursor.execute('CREATE TABLE IF NOT EXISTS finished_projects (id INTEGER PRIMARY KEY, name TEXT, directory TEXT, link TEXT)')
        except sqlite3.OperationalError as e:
            print(f'Error: Unable to create finished table. {e}')
            return
        # Move the project to the finished projects table
        try:
            self.cursor.execute('INSERT INTO finished_projects (name, directory, link) SELECT name, directory, link FROM projects WHERE id = ?', (id,))
            self.cursor.execute('DELETE FROM projects WHERE id = ?', (id,))
            self.connection.commit()
            print('... done!')
        except sqlite3.IntegrityError as e:
            print(f'Error: Unable to add project to database. {e}')
        
    def remove_project_name(self, name):
        print('Removing project from database...')
        # Create finished_projects table if it doesn't exist
        try:
            self.cursor.execute('CREATE TABLE IF NOT EXISTS finished_projects (id INTEGER PRIMARY KEY, name TEXT, directory TEXT, link TEXT)')
        except sqlite3.OperationalError as e:
            print(f'Error: Unable to create finished table. {e}')
            return
        # Move the project to the finished projects table
        try:
            self.cursor.execute('INSERT INTO finished_projects (name, directory, link) SELECT name, directory, link FROM projects WHERE name =?', (name,))
            self.cursor.execute('DELETE FROM projects WHERE name =?', (name,))
            self.connection.commit()
            print('... done!')
        except sqlite3.IntegrityError as e:
            print(f'Error: Unable to add project to database. {e}')


    def create_table(self, table_name):
        try:
            self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} \
                    (id INTEGER PRIMARY KEY, name TEXT, directory TEXT, link TEXT)')

        except sqlite3.OperationalError as e:
            print(f'Error: Unable to create {table_name} table. {e}')
            return
        
    def get_project_info(self, idenifier, project):
        if idenifier == 'name':
            try:
                self.cursor.execute(f'SELECT * FROM projects WHERE name =?', (project,))
                return self.cursor.fetchone()
            except:
                print('Error: Unable to get project info.')
                return

        if idenifier == 'id':
            try:
                self.cursor.execute(f'SELECT * FROM projects WHERE id =?', (project,))
                return self.cursor.fetchone()
            except:
                print('Error: Unable to get project info.')
                return