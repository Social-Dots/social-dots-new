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

# Simple database setup for Vercel
def setup_vercel_database():
    """Simple database setup for Vercel deployment"""
    try:
        from django.core.management import call_command
        from core.models import SiteConfiguration
        
        print("🔍 Checking database status...")
        
        # Run migrations first
        print("📦 Running migrations...")
        call_command('migrate', verbosity=0)
        print("✅ Migrations complete")
        
        # Check if we have basic configuration
        if not SiteConfiguration.objects.exists():
            print("🔧 Creating basic site configuration...")
            SiteConfiguration.objects.create(
                site_name="Social Dots Inc",
                tagline="AI Integration & Digital Marketing",
                contact_email="info@socialdots.ca",
                contact_phone="+1 (416) 123-4567",
                address="123 Tech Street, Toronto, ON M5V 1A1"
            )
            print("✅ Basic configuration created")
        else:
            print("✅ Site configuration exists")
            
        print("🎉 Database setup complete!")
            
    except Exception as e:
        print(f"⚠️ Database setup error: {e}")
        # Continue anyway - don't break the app

# Check if running on Vercel
is_vercel = (
    os.environ.get('VERCEL') or 
    os.environ.get('VERCEL_URL') or
    os.environ.get('LAMBDA_TASK_ROOT') or
    os.environ.get('VERCEL_ENV')
)

if is_vercel:
    print("📦 Vercel environment detected - setting up database...")
    setup_vercel_database()
else:
    print("🏠 Local environment detected")

# Get the WSGI application
application = get_wsgi_application()

# Vercel handler
app = application