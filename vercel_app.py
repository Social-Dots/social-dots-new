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
                print("🔍 No site configuration found - database needs setup")
                needs_setup = True
            else:
                print(f"✅ Site configuration found: {site_config.site_name}")
                
                # Check for content
                from core.models import BlogPost, Project, Portfolio
                blog_count = BlogPost.objects.count()
                project_count = Project.objects.count() 
                portfolio_count = Portfolio.objects.count()
                
                print(f"📊 Content count - Blogs: {blog_count}, Projects: {project_count}, Portfolio: {portfolio_count}")
                
                if blog_count == 0 and project_count == 0 and portfolio_count == 0:
                    print("📋 Configuration exists but no content found - loading content...")
                    needs_setup = True
                else:
                    needs_setup = False
        except Exception as db_error:
            print(f"🔍 Database check error: {db_error}")
            needs_setup = True
            
        if needs_setup:
            print("🚀 Setting up Vercel database with content...")
            
            # Run migrations
            print("📦 Running migrations...")
            call_command('migrate', verbosity=1)
            print("✅ Migrations complete")
            
            # Try complete localhost sync first (your actual working localhost)
            print("🔄 Attempting COMPLETE localhost database sync...")
            try:
                call_command('complete_localhost_sync', '--force', verbosity=1)
                print("✅ Complete localhost database sync successful")
            except Exception as sync_error:
                print(f"⚠️ Complete sync failed: {sync_error}")
                
                # Try partial production data as backup
                print("🔄 Trying partial production data loading...")
                try:
                    call_command('load_production_data', verbosity=1)
                    print("✅ Partial production data loaded")
                except Exception as prod_error:
                    print(f"⚠️ Production data loading failed: {prod_error}")
                    print("🔄 Falling back to demo content setup...")
                    
                    # Final fallback to demo content
                    print("⚙️ Setting up site configuration...")
                    call_command('setup_socialdots', verbosity=1)
                    print("✅ Site configuration and services created")
                    
                    print("📝 Loading demo content...")
                    call_command('load_demo_content', verbosity=1) 
                    print("✅ Demo blog posts and portfolio loaded")
                    
                    print("💰 Loading demo pricing...")
                    call_command('load_demo_pricing', verbosity=1)
                    print("✅ Demo pricing plans loaded")
            
            # Final count check
            from core.models import BlogPost, Project, Portfolio
            final_blog_count = BlogPost.objects.count()
            final_project_count = Project.objects.count() 
            final_portfolio_count = Portfolio.objects.count()
            
            print(f"🎯 Final content count - Blogs: {final_blog_count}, Projects: {final_project_count}, Portfolio: {final_portfolio_count}")
            print("🎉 Database setup complete!")
        else:
            print("✅ Database already configured")
            
    except Exception as e:
        print(f"⚠️ Database setup error: {e}")
        # Continue anyway - don't break the app

# Run database setup on cold start
print("🔍 Environment check:")
print(f"VERCEL env var: {os.environ.get('VERCEL')}")
print(f"VERCEL_URL env var: {os.environ.get('VERCEL_URL')}")
print(f"LAMBDA_TASK_ROOT: {os.environ.get('LAMBDA_TASK_ROOT')}")
print(f"AWS_LAMBDA_FUNCTION_NAME: {os.environ.get('AWS_LAMBDA_FUNCTION_NAME')}")

# Check multiple ways Vercel might be detected
is_vercel = (
    os.environ.get('VERCEL') or 
    os.environ.get('VERCEL_URL') or
    os.environ.get('LAMBDA_TASK_ROOT') or  # Vercel serverless functions
    'vercel' in os.environ.get('HOSTNAME', '').lower() or
    '/var/task' in str(Path(__file__).resolve())  # Vercel lambda path
)

if is_vercel:
    print("📦 Detected Vercel/serverless environment - setting up database...")
    setup_vercel_database()
else:
    print("🏠 Running in local environment")
    # Even in local, check if we need content for development
    try:
        from core.models import BlogPost
        if BlogPost.objects.count() == 0:
            print("🔧 No content found in local development - running setup...")
            setup_vercel_database()
    except Exception as e:
        print(f"🔍 Local content check failed: {e}")

# Get the WSGI application
application = get_wsgi_application()

# Vercel handler
app = application