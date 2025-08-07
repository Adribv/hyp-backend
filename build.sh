#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Starting build process..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create necessary directories (with error handling)
echo "Creating directories..."
mkdir -p src/api/uploads || echo "Warning: Could not create uploads directory"
mkdir -p src/api/logs || echo "Warning: Could not create logs directory"
mkdir -p src/db || echo "Warning: Could not create db directory"

# Set permissions (with error handling)
echo "Setting permissions..."
chmod +x src/startup.py || echo "Warning: Could not set startup.py permissions"

echo "Build process completed successfully!"
