
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
    echo "Usage: $0 -cmd <command> -name <project_name>"
    echo "Short options: $0 -c <command> -n <project_name>"
    exit 1
}
open_cmd_usage() {
    echo "Usage: $0 -cmd <command> -name <project_name>"
    echo "Short options: $0 -c <command> -n <project_name>"
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
        -h|--help)
            command="help"
            shift 1
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

# Check if all required options are provided
if [ -z "$command" ]; then
    echo "Error: Command is required." >&2
    exit 1
fi

if [ "$command" = "help" ]; then
    python3 src/main.py "$command"
fi

if [ "$command" = "new" ]; then
    if [ "$project_name" = "None" ] || [ "$working_directory" = "None" ] || [ "$project_link" = "None" ]; then
        new_cmd_usage
    fi
    python3 src/main.py "$command" "$project_name" "$working_directory" "$project_link"
    echo "Executing new command..."
elif [ "$command" = "todo" ]; then
    python3 src/main.py "$command"
    echo "Executing todo command..."
elif [ "$command" = "finish" ]; then
    if [ "$project_name" = "None" ]; then
        finish_cmd_usage
    fi
    python3 src/main.py "$command" "$project_name"
    echo "Executing finish command..."
elif [ "$command" = "open" ]; then
    if [ "$project_name" = "None" ]; then
        open_cmd_usage
    fi
    python3 src/main.py "$command" "$project_name"
    echo "Executing open command..."
fi

