import os
import sys
from pathlib import Path

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

# Auto-setup database and content on Vercel deployment
def setup_vercel_database():
    """Setup database with migrations and demo content for Vercel deployment"""
    try:
        from django.core.management import call_command
        from django.db import connection
        from core.models import SiteConfiguration
        
        # Check if database is empty (needs setup)
        try:
            site_config = SiteConfiguration.objects.first()
            if not site_config:
                needs_setup = True
            else:
                needs_setup = False
        except:
            needs_setup = True
            
        if needs_setup:
            print("🚀 Setting up Vercel database with content...")
            
            # Run migrations
            call_command('migrate', verbosity=0)
            print("✅ Migrations complete")
            
            # Setup initial data
            call_command('setup_socialdots', verbosity=0)
            print("✅ Site configuration and services created")
            
            # Load demo content
            call_command('load_demo_content', verbosity=0) 
            print("✅ Demo blog posts and portfolio loaded")
            
            # Load demo pricing
            call_command('load_demo_pricing', verbosity=0)
            print("✅ Demo pricing plans loaded")
            
            print("🎉 Database setup complete!")
        else:
            print("✅ Database already configured")
            
    except Exception as e:
        print(f"⚠️ Database setup error: {e}")
        # Continue anyway - don't break the app

# Run database setup on cold start
if os.environ.get('VERCEL'):
    setup_vercel_database()

# Get the WSGI application
application = get_wsgi_application()

# Vercel handler
app = application