import os
import sys

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialdots.settings')

# Setup Django
import django
django.setup()

# Initialize database for in-memory SQLite
from django.conf import settings
if settings.DATABASES['default']['NAME'] == ':memory:':
    from django.core.management import call_command
    try:
        # Run migrations
        call_command('migrate', verbosity=0)
        # Load initial data
        call_command('setup_socialdots', verbosity=0)
    except Exception as e:
        print(f"Database initialization error: {e}", file=sys.stderr)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
app = application