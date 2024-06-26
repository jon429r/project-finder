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
- Setup the Bash and zshell environment  by running chmod +x setup_env.sh && ./setup_env.sh
- then run the code with the bash or zsh command TODO

## Bugs

As the project is still in development, there maybe a few identified bugs:


## Plans for the Future

Future plans for Project-Finder include:

- **GUI:** **In development** Develop a graphical user interface for a more user-friendly experience, moving away from the command line.
- **Migration to MySQL:** Transfer data to a MySQL server, introducing user entities with passwords and usernames.
- **Bug Fixes:** Prioritize fixing existing bugs before implementing new features.


## Commands

As this is an application used through the Mac Terminal here are the commands for the application 

I'm currently working on implementing a GIU run this by Using the command TODO -gui

    1. Create a new project: todo --cmd new --name <"project_name"> --dir <"working_directory"> 
    or todo -c new -n <"project_name"> -d <"working_directory"> -l <"project_link">
    working_directory and link are optional but recommended
    please insert the whole directory path starting with a '/'
    2. View existing projects: todo -cmd todo or todo -c todo
    3. Finished an existing project: todo -cmd finish -name <project_name> 

    or todo -c finish -n <project_name>
    4. Open an existing project: todo -cmd open -name <project_name> 
    or todo -c open -n <project_name>
    6. todo -cmd Help or todo -c Help

    4. Open an existing project: todo -cmd open -name <project_name>  
    6. Todo -cmd Help 

## Compatibility

Written and tested in python 3.10.10, on MacOS, for MacOS and Linux, Zsh and bash terminal

## Requirments

sqlite3, python3, zsh, bash
