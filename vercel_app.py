import os
import sys

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialdots.settings')

try:
    # Setup Django
    import django
    django.setup()

    # Initialize database for in-memory SQLite
    from django.conf import settings
    if settings.DATABASES['default']['NAME'] == ':memory:':
        from django.core.management import call_command
        try:
            # Run migrations silently
            call_command('migrate', verbosity=0, interactive=False)
            # Load initial data
            call_command('setup_socialdots', verbosity=0)
        except Exception as e:
            print(f"Database initialization warning: {e}", file=sys.stderr)

    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    app = application

except Exception as e:
    print(f"Django initialization error: {e}", file=sys.stderr)
    # Create a minimal WSGI application as fallback
    def simple_app(environ, start_response):
        status = '503 Service Unavailable'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return [b'Service temporarily unavailable']

    app = simple_app