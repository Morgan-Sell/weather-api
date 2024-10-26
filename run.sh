#!/bin/bash

# Exit on error
set -e

# Ensures the the script always points to the directory in which the script is located
THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Set Python Path
export PYTHONPATH=$THIS_DIR

# Function to open the default web browser with a specified URL
function open-browser {
    local url=$1
    echo "Opening browser at $url..."

    # Check the operating system and open the browser with the appropriate command
    if which xdg-open > /dev/null; then
        xdg-open "$url"  # For Linux
    elif which open > /dev/null; then
        open "$url"      # For macOS
    elif which start > /dev/null; then
        start "$url"     # For Windows (Git Bash or Cygwin)
    else
        echo "Please manually open a browser and navigate to $url"
    fi
}

# Run application once configuration is setup
function run-app {
    # echo "Running application with PYTHONPATH=$PYTHONPATH"
    python src/main.py
}


# Load environment variables from .env file
function load-env {
    if [ -f "$THIS_DIR/.env" ]; then
        echo "Loading environment variables from .env file..."
        export $(cat "$THIS_DIR/.env" | xargs)
    else
        echo ".env file not found! Create one and include GITHUB_TOKEN."
        exit 1
    fi
}

# Check for GitHub token
function check-github-token {
    load-env
    if [ -z "$GITHUB_TOKEN"]; then
        echo "GITHUB_TOKEN is not set. Add it to your .env file."
        exit 1
    fi
}

# Set up a virtual environment
function setup-venv {
    if [ ! -d "venv" ]; then
        python3.11 -m venv venv
        echo "Virtual environment created."
    fi
    source venv/bin/activate
    echo "Virtual environment activated."
}

# Install dependencies
function install-deps {
    setup-venv
    pip install --upgrade pip
    pip install -r requirements.txt

}

# Run all setup tasks after cloning the repo
function initial-setup {
    echo "Running initial setup..."
    check-github-token
    setup-venv
    install-deps
    echo "Initial setup completed. You're ready to go!"
}

# Display help/usage information
function help {
    echo "Usage: ./run.sh <task>"
    echo "Tasks:"
    echo "  run-app             Run the application"
    echo "  load-env            Load environment variables from .env"
    echo "  setup-venv          Set up virtual environment"
    echo "  install-deps        Install dependencies"
    echo "  initial-setup       Run the initial setup after cloning"
    echo "  help                Show this help message"
}

# Main script logic for running the desired task
if [ $# -eq 0 ]; then
    help
    exit 0
fi

case "$1" in
    run-app)
        run-app
        ;;
    load-env)
        load-env
        ;;
    check-github-token)
        check-github-token
        ;;
    setup-venv)
        setup-venv
        ;;
    install-deps)
        install-deps
        ;;
    initial-setup)
        initial-setup
        ;;
    help)
        help
        ;;
    *)
        echo "Invalid task: $1"
        help
        exit 1
        ;;
esac