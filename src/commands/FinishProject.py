"""
finish_project.py.

This module contains the class for the finish command.
"""

import logging
import sqlite3
from sys import argv

from database import Database as dataclass
from Logger import Logger


class FinishedProject:
    """This class provides the functionality to finish a project."""

    def __init__(self):
        """Initialize the FinishedProject class."""
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()
        self.db = dataclass()

    @Logger.log_action(action="Finish project", severity=logging.DEBUG)
    def finish_project(self):
        """
        Defines the command function.

        :param user_input: The user input to parse and execute.
        """
        if argv[2].isdigit():
            project_id = argv[2]
            print(f"Project ID: {project_id}")
            project_info = self.db.get_project_info("id", project_id)
            print(project_info)
        else:
            project_name = argv[2]
            project_info = self.db.get_project_info("name", project_name)
            if project_info is None:
                print("Project not found")
            else:
                project_id = project_info[0]
                print(project_id)

        print("Please confirm the details above are correct.")
        confirm = False
        while not confirm:
            confirm = input("Y/N")

            if confirm == "Y":
                self.db.remove_project("id", project_id)
            elif confirm == "N":
                print("Canceling project deletion...")
                print("... Canceled!")
            else:
                print("Invalid input, please try again.")
        return

    def helper(self):
        """Defines the Helper function."""
        pass
