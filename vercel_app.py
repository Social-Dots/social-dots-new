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
            
            # Setup initial data
            print("⚙️ Setting up site configuration...")
            call_command('setup_socialdots', verbosity=1)
            print("✅ Site configuration and services created")
            
            # Load demo content
            print("📝 Loading demo content...")
            call_command('load_demo_content', verbosity=1) 
            print("✅ Demo blog posts and portfolio loaded")
            
            # Load demo pricing
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
print("🔍 Vercel environment check:")
print(f"VERCEL env var: {os.environ.get('VERCEL')}")
print(f"Python path: {sys.path}")

if os.environ.get('VERCEL'):
    print("📦 Running in Vercel environment - setting up database...")
    setup_vercel_database()
else:
    print("🏠 Running in local environment - skipping database setup")

# Get the WSGI application
application = get_wsgi_application()

# Vercel handler
app = application