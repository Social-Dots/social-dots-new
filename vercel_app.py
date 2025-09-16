# Ultra-minimal test WSGI app for debugging
def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/html')]
    start_response(status, headers)

    # Try to import Django and show any errors
    try:
        import django
        django_version = django.VERSION

        import os
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialdots.settings')
        django.setup()

        from django.conf import settings
        db_name = settings.DATABASES['default']['NAME']

        content = f"""
        <h1>Social Dots - Debug Test</h1>
        <p>OK Python import works</p>
        <p>OK Django version: {django_version}</p>
        <p>OK Django setup successful</p>
        <p>OK Database: {db_name}</p>
        <p>If you see this, basic Django setup is working!</p>
        """

    except Exception as e:
        content = f"""
        <h1>Social Dots - Debug Test</h1>
        <p>ERROR Error occurred: {str(e)}</p>
        <p>Error type: {type(e).__name__}</p>
        """

    return [content.encode('utf-8')]

# Vercel expects 'app'
app = application