#!/bin/bash
#
#
# inorder to run this steps you need to complete the following steps:
# chmod +x /Users/jonathanday/Documents/GitHub/Project-finder/todo.sh
# sudo ln -s /Users/jonathanday/Documents/GitHub/Project-finder/todo.sh /usr/local/bin/todo > This will create a symbolic link to the script so you can run without .sh from anywhere
#
# export PATH="/Users/jonathanday/Documents/GitHub/Project-finder:$PATH" >> Add this to your .bash_profile or .zshrc
# source ~/.bash_profile > to reload profiles
# source ~/.zshrc
#

# Determine current working directory
current_directory=$(pwd)

# Determine paths based on current directory
todo_script_path="$current_directory/todo.sh"
link_destination_path="/usr/local/bin/todo"
bash_profile_path="$HOME/.bash_profile" 
zsh_profile_path="$HOME/.zshrc"

# Step 1: Make the script executable
chmod +x "$todo_script_path"


# Step 2: Add the script directory to the PATH in profile file
echo "export PATH=\"$current_directory:\$PATH\"" >> "$profile_path"
echo "export PATH=\"$current_directory:\$PATH\"" >> "$zsh_profile_path"

# Step 3: Reload the shell profiles
source "$profile_path"

# Step 4: Create a symbolic link to the script
sudo ln -s "$todo_script_path" "$link_destination_path"


echo "Setup completed successfully."
