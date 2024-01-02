#!/bin/bash

required_python_version="3.7"

# Check if Python 3.7 or newer is installed
if command -v python3 &>/dev/null; then
    installed_python_version=$(python3 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")

    if [[ "${installed_python_version}" < "${required_python_version}" ]]; then
        echo "Python ${required_python_version} or newer is required, but version ${installed_python_version} is installed."
        echo "Installing Python ${required_python_version}..."
        
        # Install Python 3.7 or newer based on the package manager
        if command -v apt-get &>/dev/null; then
            sudo apt-get update
            sudo apt-get install -y python3.7
        elif command -v yum &>/dev/null; then
            sudo yum install -y python3
        elif command -v brew &>/dev/null; then
            brew install python@3.7
        else
            echo "Unsupported package manager. Please install Python ${required_python_version} manually."
            exit 1
        fi

        echo "Python ${required_python_version} installed successfully."
    else
        echo "Python ${required_python_version} or newer is already installed."
    fi
else
    echo "Python 3.7 or newer is not installed."
    echo "Please install Python ${required_python_version} manually."
    exit 1
fi
