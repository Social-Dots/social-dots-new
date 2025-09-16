import os
import sys
from pathlib import Path
import django
from django.core.wsgi import get_wsgi_application

# Add project root to Python path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

# Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialdots.settings')
django.setup()

def setup_fresh_deployment():
    """Load complete localhost data on fresh Vercel deployment"""
    try:
        from django.core.management import call_command
        from core.models import SiteConfiguration, BlogPost
        
        print("🚀 FRESH VERCEL DEPLOYMENT SETUP")
        
        # Run migrations first
        print("📦 Running migrations...")
        call_command('migrate', verbosity=0)
        print("✅ Migrations complete")
        
        # Check if data already exists
        if SiteConfiguration.objects.exists() and BlogPost.objects.count() > 5:
            print("✅ Data already loaded - skipping setup")
            return
        
        # Load complete localhost data
        data_file = project_root / 'complete_localhost_data.json'
        if data_file.exists():
            print("📥 Loading complete localhost data...")
            call_command('loaddata', str(data_file), verbosity=0)
            print("✅ Complete localhost data loaded successfully!")
            
            # Verify data loaded correctly
            blog_count = BlogPost.objects.count()
            print(f"✅ Loaded {blog_count} blog posts")
        else:
            print("⚠️ Data file not found - creating minimal setup")
            # Create minimal site config if no data file
            if not SiteConfiguration.objects.exists():
                SiteConfiguration.objects.create(
                    site_name="Social Dots Inc",
                    tagline="AI Integration & Digital Marketing",
                    contact_email="info@socialdots.ca"
                )
                print("✅ Basic configuration created")
        
        print("🎉 Fresh deployment setup complete!")
        
    except Exception as e:
        print(f"⚠️ Setup error: {e}")
        # Continue anyway to not break the app

# Check if this is Vercel
is_vercel = bool(
    os.environ.get('VERCEL') or 
    os.environ.get('VERCEL_URL') or 
    os.environ.get('LAMBDA_TASK_ROOT')
)

if is_vercel:
    print("🔍 Vercel detected - setting up fresh deployment...")
    setup_fresh_deployment()
else:
    print("🏠 Local environment")

# WSGI application
application = get_wsgi_application()
app = application