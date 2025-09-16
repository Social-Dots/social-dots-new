import os
import sys

# Add project directory to Python path
try:
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(project_root)
except NameError:
    # Handle case when __file__ is not defined (e.g., interactive mode)
    pass

# Set Django environment variables
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialdots.settings')
os.environ.setdefault('DEBUG', 'False')
os.environ.setdefault('DATABASE_URL', 'sqlite:///:memory:')
os.environ.setdefault('SECRET_KEY', 'django-vercel-deployment-key-2024')

# Setup Django
import django
django.setup()

# Run database setup for in-memory SQLite
from django.core.management import call_command
from django.conf import settings

if settings.DATABASES['default']['NAME'] == ':memory:':
    try:
        call_command('migrate', verbosity=0, interactive=False)
        call_command('setup_socialdots', verbosity=0)
    except Exception as e:
        print(f"Database setup warning: {e}")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Vercel expects 'app'
app = application