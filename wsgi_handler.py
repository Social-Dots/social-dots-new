import os
import sys
from pathlib import Path

# Django WSGI Handler for Vercel Deployment
# Created: 2025-09-09 - Force rebuild for markdownify fix

# Add the project root to Python path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialdots.settings')

# Import Django after setting up the path and environment
import django
from django.core.wsgi import get_wsgi_application

# Configure Django
django.setup()

# Get the WSGI application
application = get_wsgi_application()

# Vercel handler
app = application