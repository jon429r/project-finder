import sqlite3

import pytest
from project.database import Database as Database


# Pytest fixture to create a temporary database connection
@pytest.fixture
def temp_database(tmp_path):
    # Create a temporary database file in a temporary directory
    db_path = tmp_path / "test_database.db"

    # Instantiate the database class and initialize the database
    db_instance = Database(db_name=str(db_path))
    yield db_instance
    db_instance.connection.close()


def test_new_project(temp_database):
    # Arrange
    db = temp_database
    name = "TestProject"
    directory = "/path/to/project"
    link = "https://github.com/testproject"

    # Act
    db.new_project(name, directory, link)

    # Assert
    result = db.get_project_info("name", name)
    assert result is not None
    assert result is not 400
    assert result[1] == name
    assert result[2] == directory
    assert result[3] == link


def test_remove_project_id(temp_database):
    # Arrange
    db = temp_database
    name = "TestProject"
    directory = "/path/to/project"
    link = "https://github.com/testproject"

    # Act
    db.new_project(name, directory, link)
    project_info = db.get_project_info("name", name)
    project_id = project_info[0]
    db.remove_project_id(project_id)

    # Assert
    result = db.get_project_info("id", project_id)
    assert result is None
    assert result is not 400


def test_remove_project_name(temp_database):
    # Arrange
    db = temp_database
    name = "TestProject"
    directory = "/path/to/project"
    link = "https://github.com/testproject"

    # Act
    db.new_project(name, directory, link)
    db.remove_project_name(name)

    # Assert
    result = db.get_project_info("name", name)
    assert result is None
    assert result is not 400


from project.finish_project import finished_project


def test_finish_project(temp_database):
    # Arrange
    db = temp_database
    name = "TestProject"
    directory = "/path/to/project"
    link = "www.github.com/testproject"

    # Act
    db.new_project(name, directory, link)

    # Instantiate finished_project class using the corrected class name
    fp = finished_project()

    # Assert
    result = db.get_project_info("name", name)
    assert result is None
