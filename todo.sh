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
        -h|--help|?)
            command="help"
            shift 1
            ;;
        -v|--verbose)
            verbose="True"
            shift 1
            ;;
        *)
            echo "Unknown option: $1" >&2
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
    exit 1
fi

if [ "$command" = "help" ]; then
    if [ "$verbose" = "True" ]; then
        python3 "/src/main.py" "$command" -v
    else
        python3 "/src/main.py"  "$command" 
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

