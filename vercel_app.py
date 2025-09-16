import os
import sys
import traceback
from pathlib import Path

print("🚀 VERCEL DEPLOYMENT STARTING")
print(f"Python version: {sys.version}")
print(f"Current working directory: {os.getcwd()}")

try:
    # Add project root to Python path
    project_root = Path(__file__).resolve().parent
    sys.path.insert(0, str(project_root))
    print(f"✅ Project root added to path: {project_root}")

    # Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialdots.settings')
    print("✅ Django settings module set")
    
    import django
    print(f"✅ Django imported, version: {django.VERSION}")
    
    django.setup()
    print("✅ Django setup complete")
    
    from django.core.wsgi import get_wsgi_application
    print("✅ WSGI application imported")

except Exception as e:
    print(f"❌ ERROR during Django setup: {e}")
    print(f"❌ Full traceback:\n{traceback.format_exc()}")
    raise

def setup_fresh_deployment():
    """Load complete localhost data on fresh Vercel deployment"""
    try:
        print("🚀 STARTING FRESH DEPLOYMENT SETUP")
        
        from django.core.management import call_command
        print("✅ Management commands imported")
        
        from core.models import SiteConfiguration, BlogPost
        print("✅ Models imported")
        
        # Run migrations first
        print("📦 Running migrations...")
        call_command('migrate', verbosity=1)
        print("✅ Migrations complete")
        
        # Check if data already exists
        site_config_count = SiteConfiguration.objects.count()
        blog_count = BlogPost.objects.count()
        print(f"📊 Current data: {site_config_count} site configs, {blog_count} blog posts")
        
        if site_config_count > 0 and blog_count > 5:
            print("✅ Data already loaded - skipping setup")
            return
        
        # Load complete localhost data
        data_file = project_root / 'complete_localhost_data.json'
        print(f"🔍 Looking for data file: {data_file}")
        
        if data_file.exists():
            print(f"📥 Data file found, size: {data_file.stat().st_size} bytes")
            print("📥 Loading complete localhost data...")
            call_command('loaddata', str(data_file), verbosity=1)
            print("✅ Complete localhost data loaded successfully!")
            
            # Verify data loaded correctly
            final_blog_count = BlogPost.objects.count()
            final_config_count = SiteConfiguration.objects.count()
            print(f"✅ Final count: {final_config_count} configs, {final_blog_count} blog posts")
        else:
            print("⚠️ Data file not found - creating minimal setup")
            # Create minimal site config if no data file
            if not SiteConfiguration.objects.exists():
                config = SiteConfiguration.objects.create(
                    site_name="Social Dots Inc",
                    tagline="AI Integration & Digital Marketing",
                    contact_email="info@socialdots.ca"
                )
                print(f"✅ Basic configuration created: {config.site_name}")
        
        print("🎉 Fresh deployment setup complete!")
        
    except Exception as e:
        print(f"❌ Setup error: {e}")
        print(f"❌ Setup traceback:\n{traceback.format_exc()}")
        # Continue anyway to not break the app

# Check if this is Vercel
vercel_env = os.environ.get('VERCEL')
vercel_url = os.environ.get('VERCEL_URL')  
lambda_root = os.environ.get('LAMBDA_TASK_ROOT')

print(f"🔍 Environment check:")
print(f"   VERCEL: {vercel_env}")
print(f"   VERCEL_URL: {vercel_url}")
print(f"   LAMBDA_TASK_ROOT: {lambda_root}")

is_vercel = bool(vercel_env or vercel_url or lambda_root)
print(f"🎯 IS_VERCEL: {is_vercel}")

if is_vercel:
    print("🔍 Vercel detected - setting up fresh deployment...")
    setup_fresh_deployment()
else:
    print("🏠 Local environment - skipping setup")

# WSGI application
print("🔄 Creating WSGI application...")
try:
    application = get_wsgi_application()
    print("✅ WSGI application created successfully")
    app = application
    print("✅ App exported for Vercel")
except Exception as e:
    print(f"❌ WSGI creation failed: {e}")
    print(f"❌ WSGI traceback:\n{traceback.format_exc()}")
    raise

print("🎉 VERCEL DEPLOYMENT COMPLETE!")