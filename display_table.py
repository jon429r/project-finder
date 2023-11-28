from tabulate import tabulate
import os
import sqlite3

cursor = sqlite3.connect('database.db')

id = cursor.execute('SELECT id FROM projects')
project_name = cursor.execute('SELECT name FROM projects')
working_directory = cursor.execute('SELECT directory FROM projects')

table = [[id , project_name, working_directory],]

print(tabulate(table, headers=['id' 'Project', 'Directory'], tablefmt='grid'))

