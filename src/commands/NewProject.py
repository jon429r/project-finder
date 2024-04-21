"""This file is responsible for creating a new project in the database."""

import logging
import sqlite3
from sys import argv

from database import Database as dataclass
from Logger import Logger


@Logger.log_action(action="Parsing project info", severity=logging.DEBUG)
def parse_project_info() -> tuple:
    """
    Parses project info from command line arguments.

    returns: Tuple: (project_name, working_directory, project_link)
    """
    try:
        project_name = argv[2] if argv[2] != "None" else None
        working_directory = argv[3] if argv[3] != "None" else None
        project_link = argv[4] if argv[4] != "None" else None

        if project_name is None:
            print("Error: Please specify a project name.")
            return

        print(f"""Project name: {project_name} Dir: {working_directory}
           Link: {project_link}""")
    except Exception as e:
        print(f"Error: Unable to parse project info. {e}")
        return

    return project_name, working_directory, project_link


class NewProject:
    """This class provides the functionality to create a new project."""

    def __init__(self):
        """Initalizes new project class."""
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()

    @Logger.log_action(action="Creating a new project", severity=logging.INFO)
    def new_project(self):
        """
        Command function.

        :param cmd: The user input to parse and execute.
        """
        db = dataclass()
        print("Creating a new project...")
        try:
            db.create_table(table_name="projects")
        except TypeError as e:
            print(f"Error: Unable to create table. {e}")
            return 400

        project_name, working_directory, project_link = parse_project_info()
        if project_name is None:
            return 400

        print("Please confirm the details above are correct.")
        confirm = False
        while confirm is False:
            confirmation = input("Y/N")

            if confirmation == "Y":
                print("Adding project to database...")
                try:
                    # Create finished_projects table if it doesn't exist
                    db.create_table("projects")
                    db.new_project(
                        name=project_name,
                        directory=working_directory,
                        link=project_link,
                    )
                except Exception as e:
                    print(f"Error: Unable to add project to database.{e}")
                    return 400
                print("... done!")
                confirm = True
            elif confirm == "N":
                print("Canceling project creation...")
                print("... Canceled!")
                confirm = True
            else:
                print("Invalid input, please try again.")
        return
