import sqlite3

class database:
    def __init__(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()

    def new_project(self, name, directory, link):
        self.cursor.execute('INSERT INTO projects (name, directory, link) VALUES (?, ?, ?)'
            , (name, directory, link))

        self.connection.commit()


    def remove_project_id(self, id):
        print('Removing project from database...')
        # Create finished_projects table if it doesn't exist
        self.cursor.execute('CREATE TABLE IF NOT EXISTS finished_projects (id INTEGER PRIMARY KEY, name TEXT, directory TEXT, link TEXT)')
        # Move the project to the finished projects table
        self.cursor.execute('INSERT INTO finished_projects (name, directory, link) SELECT name, directory, link FROM projects WHERE id = ?', (id,))
        self.cursor.execute('DELETE FROM projects WHERE id = ?', (id,))
        self.connection.commit()
        print('... done!')
        
    def remove_project_name(self, name):
        print('Removing project from database...')
        # Create finished_projects table if it doesn't exist
        self.cursor.execute('CREATE TABLE IF NOT EXISTS finished_projects (id INTEGER PRIMARY KEY, name TEXT, directory TEXT, link TEXT)')
        # Move the project to the finished projects table
        self.cursor.execute('INSERT INTO finished_projects (name, directory, link) SELECT name, directory, link FROM projects WHERE name = ?', (name,))
        self.cursor.execute('DELETE FROM projects WHERE name = ?', (name,))
        self.connection.commit()
        print('... done!')

    def create_table(self, table_name):
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} \
                (id INTEGER PRIMARY KEY, name TEXT, directory TEXT, link TEXT)')