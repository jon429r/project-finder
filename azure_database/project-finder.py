import os
import pyodbc, struct
from azure import identity

from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Connection parameters
server = 'project-finder.database.windows.net'
database = 'Project-Finder'
username = 'jonathanday088'
password = 'Jonandtee22!'
driver = '{ODBC Driver 17 for SQL Server}'  # Use the appropriate driver

# Create a connection string
connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

try:
    # Establish a connection
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    # Execute SQL queries
    cursor.execute('SELECT @@version')
    row = cursor.fetchone()
    while row:
        print(row[0])
        row = cursor.fetchone()

    # Close cursor and connection
    cursor.close()
    connection.close()

except pyodbc.Error as e:
    print(f'Error: {str(e)}')

