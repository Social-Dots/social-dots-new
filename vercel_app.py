import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialdots.settings')

import django
django.setup()

# Run migrations for in-memory database
from django.core.management import call_command
from django.conf import settings

if settings.DATABASES['default']['NAME'] == ':memory:':
    call_command('migrate', verbosity=0, interactive=False)
    call_command('setup_socialdots', verbosity=0)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Vercel expects 'app'
app = application