
#!/bin/bash

# Usage message
new_cmd_usage() {
    echo "Usage: $0 -cmd <command> -name <project_name> -dir <working_directory> -link <project_link>"
    exit 1
}
todo_cmd_usage() {
    echo "Usage: $0 -cmd <command>"
    exit 1
}
finish_cmd_usage() {
    echo "Usage: $0 -cmd <command> -name <project_name>"
    exit 1
}
open_cmd_usage() {
    echo "Usage: $0 -cmd <command> -name <project_name>"
    exit 1
}

working_directory="None"
project_link="None"

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -cmd)
            command="$2"
            shift 2
            ;;
        -name)
            project_name="$2"
            shift 2
            ;;
        -dir)
            working_directory="$2"
            shift 2
            ;;
        -link)
            project_link="$2"
            shift 2
            ;;
        *)
            # Unknown option
            usage
            ;;
    esac
done

# Check if all required options are provided



if [ "$command" = "new" ]; then
    if [ -z "$project_name" ] || [ -z "$working_directory" ] || [ -z "$project_link" ]; then
        new_cmd_usage
    fi


    python3 /Users/jonathanday/Documents/GitHub/Project-finder/src/main.py "$command" "$project_name" "$working_directory" "$project_link"
    echo "Executing new command..."
    exit 0

elif [ "$command" = "todo" ]; then
    if [ -z "$command" ]; then
        todo_cmd_usage
    fi
    python3 /Users/jonathanday/Documents/GitHub/Project-finder/src/main.py "$command"
    echo "Executing todo command..."
    exit 0

elif [ "$command" = "finish" ]; then
    if  [ -z "$project_name" ]; then
        finish_cmd_usage
    fi
    python3 /Users/jonathanday/Documents/GitHub/Project-finder/src/main.py "$command" "$project_name"
    echo "Executing finish command..."
    exit 0

elif [ "$command" = "open" ]; then
    if [ -z "$project_name" ]; then
        open_cmd_usage
    fi
    python3 /Users/jonathanday/Documents/GitHub/Project-finder/src/main.py "$command" "$project_name"
    echo "Executing open command..."
    exit 0

fi


# Run Python script with arguments
#
# inorder to run this steps you need to complete the following steps:
# chmod +x /Users/jonathanday/Documents/GitHub/Project-finder/todo.sh
# sudo ln -s /Users/jonathanday/Documents/GitHub/Project-finder/todo.sh /usr/local/bin/todo > This will create a symbolic link to the script so you can run without .sh from anywhere
#
# export PATH="/Users/jonathanday/Documents/GitHub/Project-finder:$PATH" >> Add this to your .bash_profile or .zshrc
# source ~/.bash_profile > to reload profiles
# source ~/.zshrc
#
python3 /Users/jonathanday/Documents/GitHub/Project-finder/src/main.py "$command" "$project_name" "$working_directory" "$project_link"

