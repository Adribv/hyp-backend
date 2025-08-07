#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p src/api/uploads
mkdir -p src/api/logs

# Set permissions
chmod +x src/startup.py
