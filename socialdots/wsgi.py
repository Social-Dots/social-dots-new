import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialdots.settings')

# Initialize Django
import django
django.setup()

# Run migrations for in-memory database
from django.core.management import call_command
try:
    call_command('migrate', verbosity=0, interactive=False)
except:
    pass

application = get_wsgi_application()

# For Vercel
app = application