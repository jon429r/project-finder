#!/bin/bash

# Usage message
new_cmd_usage() {
    echo "Usage: $0 -cmd <command> -name <project_name> -dir <working_directory> -link <project_link>"
    echo "Short options: $0 -c <command> -n <project_name> -d <working_directory> -l <project_link>"
    exit 1
}
todo_cmd_usage() {
    echo "Usage: $0 -cmd <command>"
    echo "Short options: $0 -c <command>"
    exit 1
}
finish_cmd_usage() {
    echo "Usage: $0 -cmd <command> -name <project_name> or -id <project_id>"
    echo "Short options: $0 -c <command> -n <project_name> or -i <project_id"
    exit 1
}
open_cmd_usage() {
    echo "Usage: $0 -cmd <command> -name <project_name> or -id <project_id>"
    echo "Short options: $0 -c <command> -n <project_name> or -i <project_id"
    exit 1
}
help_cmd_verbose(){
        echo "List of available commands and uses:"

        echo "1. Create a new project:"
        echo "new --name <"proj_name"> --dir <"working_dir"> --link" 
        echo "<"proj_link">"
        echo "new -n <"project_name"> -d <"working_directory"> -l <"project_link">"
        echo "Create a new project with a specified name, working dir, and or project link."

        echo "2. View existing projects:"
        echo "todo --cmd todo"
        echo "todo -c todo"
        echo "Display a list of existing projects."

        echo "3. Finish an existing project:"
        echo "todo --cmd finish --name <project_name> or --id <project_id>"
        echo "todo -c finish -n <project_name> or -i <project_id>"
        

        echo "4. Open an existing project:"
        echo "todo --cmd open --name <project_name>"
        echo "Open an existing project by name."
        echo "Alternatively, you can open a project using its ID:"
        echo "todo --cmd open --id <project_id>"
        echo "todo -c open -n <project_name>"
        echo "todo -c open -i <project_id>"
        

        echo "5. Exit:"
        echo "exit"
        echo "Quit the application."

        echo "6. Help:"
        echo "todo --cmd help"
        echo "todo -c help"
        echo "help"
        echo "Display this help message."

        echo "Please replace placeholders like <project_name>, <working_directory>, <project_link>, and"
        echo "e <project_id> with the actual values."
}

help_cmd(){
    echo "list of commands:"

    echo "new, todo, finish, open, exit, help"

    echo "Short arguments: -n, -d, -l, -c, -i, -v"
    echo "long arguments: --name, --dir, --link, --cmd, --id, --verbose"

    echo "for a more verbose manual, add -v or --verbose to the help command"
}

working_directory="None"
project_link="None"

# parse options
while [[ $# -gt 0 ]]; do
    case "$1" in
        -c|--cmd)
            command="$2"
            shift 2
            ;;
        -i|--id)
            project_id="$2"
            shift 2
            ;;
        -n|--name)
            project_name="$2"
            shift 2
            ;;
        -d|--dir)
            working_directory="$2"
            shift 2
            ;;
        -l|--link)
            project_link="$2"
            shift 2
            ;;
        h|help|?)
            command="help"
            shift 1
            ;;
        -v|--verbose)
            verbose="True"
            shift 1
            ;;
        *)
            echo "Unknown option: $1" >&2
            echo "Use Todo h or Todo help for more information."
            exit 1
            ;;
    esac
done

script_dir="$(dirname "$(readlink -f "$0")")"

# Determine the path to the Python script
python_script="$script_dir/src/main.py"

# Check if command is provided
if [ -z "$command" ]; then
    echo "Error: Command is required." >&2
    echo "Use Todo h or Todo help for more information."
    exit 1
fi

if [ "$command" = "help" ]; then
    if [ "$verbose" = "True" ]; then
        help_cmd_verbose
    else
        help_cmd
    fi

elif [ "$command" = "new" ]; then
    # Check if all required options for new command are provided
    if [ "$project_name" = "None" ] || [ "$working_directory" = "None" ] || [ "$project_link" = "None" ]; then
        new_cmd_usage
        exit 1
    fi
    python3 "$python_script" "$command" "$project_name" "$working_directory" "$project_link"
    echo "Executing new command..."

elif [ "$command" = "todo" ]; then
    python3 "$python_script"  "$command"
    echo "Executing todo command..."

elif [ "$command" = "finish" ]; then
    # Check if either project_name or project_id is provided
    if [ "$project_name" = "None" ] && [ "$project_id" = "None" ]; then
        finish_cmd_usage
        exit 1
    fi

    if [ "$project_id" = "None" ]; then
        python3 "$python_script" "$command" "$project_name"
        echo "Executing finish command with project name..."
    else
        python3 "$python_script" "$command" "$project_id"
        echo "Executing finish command with project id..."
    fi

elif [ "$command" = "open" ]; then
    # Check if project_name is provided
    if [ "$project_name" = "None" ]; then
        open_cmd_usage
        exit 1
    fi

    # Execute open command
    python3 "$python_script" "$command" "$project_name"
    echo "Executing open command..."
else
    echo "Error: Unknown command '$command'." >&2
    exit 1
fi

