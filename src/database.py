"""This module provides an interface for interacting with SQLite database."""

import sqlite3
import logging

from Logger import Logger


class projectNotFound(Exception):
    """Raised when project is not found in the database."""


class Database:
    """This class provides an interface for interacting with SQLite database."""

    def __init__(self, db_name="database.db"):
        """
        Initialize the database and create the 'projects' table if it doesn't exist.

        :param db_name: The name of the SQLite database file.
        """
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table("projects")
        self.create_table("finished_projects")

    @Logger.log_action(action="Adding project to database", severity=logging.INFO)
    def new_project(self, name, directory, link):
        """
        Add a new project to the 'projects' table.

        :param name: The name of the project.
        :param directory: The directory of the project.
        :param link: The link to the project.
        """
        print("Adding project to database...")
        try:
            self.cursor.execute(
                "INSERT INTO projects (name, directory, link) VALUES (?, ?, ?)",
                (name, directory, link),
            )
            self.connection.commit()
        except sqlite3.IntegrityError as e:
            print(f"Error: Unable to add project to database. {e}")

    @Logger.log_action(action="Creating new table for projects", severity=logging.CRITICAL)
    def create_table(self, table_name):
        """
        Create a table if it doesn't exist.

        :param table_name: The name of the table to create.
        """
        try:
            self.cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {table_name} \
                    (id INTEGER PRIMARY KEY, name TEXT, directory TEXT, link TEXT)"
            )
        except sqlite3.OperationalError as e:
            print(f"Error: Unable to create {table_name} table. {e}")

    @Logger.log_action(action="Removing project from database", severity=logging.INFO)
    def remove_project(self, identifier, project):
        """
        Remove a project from the 'projects' table.

        :param identifier: The identifier to use to remove the project (e.g. 'id' or 'name').
        :param project: The value of the identifier.

        """
        print("Removing project from database...")
        # Move the project to the finished projects table
        try:
            self.cursor.execute(
                f"""
                INSERT INTO finished_projects (name, directory, link) 
                SELECT name, directory, link 
                FROM projects 
                WHERE {identifier} = ?
                """,
                (project,),
            )
            self.cursor.execute(
                f"""DELETE FROM projects
                                WHERE {identifier} = ?""",
                (project,),
            )
            self.connection.commit()
            print("... done!")
        except sqlite3.IntegrityError as e:
            print(f"Error: Unable to remove project to database. {e}")

    @Logger.log_action(action="Getting project info from database", severity=logging.INFO)    
    def get_project_info(self, idenifier, project):
        """
        Get information about a project from the 'projects' table.

        :param idenifier: The identifier to use to get the project info (e.g. 'id' or 'name').
        :param project: The value of the identifier.
        """
        if idenifier == "name":
            try:
                self.cursor.execute(
                    """SELECT *
                                    FROM projects
                                    WHERE name =?""",
                    (project,),
                )
                return self.cursor.fetchone()
            except projectNotFound:
                print("Error: Unable to get project info.")

        if idenifier == "id":
            try:
                self.cursor.execute(
                    """SELECT *
                                    FROM projects
                                    WHERE id =?""",
                    (project,),
                )
                return self.cursor.fetchone()
            except projectNotFound:
                print("ProjectNotFound: Unable to get project info.")

        return None
