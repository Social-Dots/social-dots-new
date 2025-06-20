import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialdots.settings')

application = get_wsgi_application()

# Add handler for Vercel deployment
app = application