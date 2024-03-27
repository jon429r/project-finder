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
echo "Current directory: $current_directory"

# Determine paths based on current directory
todo_script_path="$current_directory/todo.sh"
link_destination_path="/usr/local/bin/todo"
bash_profile_path="$HOME/.bash_profile" 
zsh_profile_path="$HOME/.zshrc"

# Step 1: Make the script executable
chmod +x "$todo_script_path"

echo making todo.sh executable


# Step 2: Add the script directory to the PATH in profile file
echo "export PATH=\"$current_directory:\$PATH\"" >> "$profile_path"
echo "export PATH=\"$current_directory:\$PATH\"" >> "$zsh_profile_path"

echo adding script to z-shell and bash configuration files

# Step 3: Reload the shell profiles
source "$profile_path"
source "$zsh_profile_path"

echo reloading shell profiles with changes

# Step 4: Create a symbolic link to the script
sudo ln -s "$todo_script_path" "$link_destination_path"
echo linking script to /usr/local/bin

echo installing pip if it does not exist...

sudo apt-get install python3-pip || sudo apt-get install python-pip

echo installing prerequisites...

pip3 install -r requirements.txt || pip install -r requirements.txt


echo "Setup completed successfully."
