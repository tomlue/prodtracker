#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Get the current directory as APP_DIR
APP_DIR=$(pwd)

# Set the path to the virtual environment's Python
VENV_PYTHON="$APP_DIR/env/bin/python"

# Create the autostart directory if it doesn't exist
mkdir -p ~/.config/autostart

# Create the desktop entry file for autostart
cat << EOF > ~/.config/autostart/tracker-app.desktop
[Desktop Entry]
Type=Application
Name=Tracker Metrics App
Exec=$VENV_PYTHON $APP_DIR/app.py &
X-GNOME-Autostart-enabled=true
Comment=Autostart for the Tracker Metrics App
Categories=Utility;
EOF

echo "Setup complete. Your app should now start automatically when you log in."
echo "To start the app manually, run:"
echo "$VENV_PYTHON $APP_DIR/app.py"
