#!/bin/bash

# Build script for Vercel deployment
echo "Building Django project..."

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput --clear

echo "Build completed!"