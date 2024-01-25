# Project-Finder

### Developer: Jonathan

## About Project-Finder

Project-Finder is a project management tool developed to address the challenges of organizing numerous programming projects. Originally conceived as a two-day project, it has evolved to encompass additional functionality. As a student and programmer, the application assists in efficiently managing project directories and associated web links.

## Technical Info

This application is built using an SQLite database to store project details, with Python handling interactions and queries. The primary entity is the project, which includes fields such as id, name, link, and directory. The id serves as the primary key, and while the project name is required, the link and directory are optional. Another entity, finished project, stores information on completed projects.

## How to Run

- Clone the repository: https://github.com/jon429r/project-finder.git
- install python if version is less than 3.7 using the provided script 'install_python3.bash'.
- Do this by running chmod +x ./install_python.bash && ./install_python.bash
- then run the code with the command 'python3 main.py'

## Bugs

As the project is still in development, there maybe a few identified bugs:


## Plans for the Future

Future plans for Project-Finder include:

- **GUI:** Develop a graphical user interface for a more user-friendly experience, moving away from the command line.
- **Migration to MySQL:** Transfer data to a MySQL server, introducing user entities with passwords and usernames.
- **Bug Fixes:** Prioritize fixing existing bugs before implementing new features.


## Commands

As this is an application used through the Mac Terminal here are the commands for the application (I do have plans for a GUI)

    1. Create a new project: new -name <"project_name"> -dir <"working_directory"> 
    please insert the whole directory path starting with a '/'
    Additional arguments: 
    -link <"project_link">
    2. View existing projects: todo 
    3. Finished an existing project: finish -name <project_name> 
    You can also remove a project by typing finish -id <project_id> 
    4. Open an existing project: open -name <project_name> 
    You can also open a project by typing open -id <project_id> 
    5. Exit 
    6. Help 

## Compatibility

Written and tested in python 3.10.10, on MacOS, Zsh terminal

## Requirments

sqlite3, python3
