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
            
            # Deploy complete localhost (your actual working website)
            print("🚀 Deploying complete localhost to Vercel...")
            try:
                call_command('deploy_complete_localhost', verbosity=1)
                print("✅ Complete localhost deployment successful")
            except Exception as deploy_error:
                print(f"⚠️ Complete localhost deployment failed: {deploy_error}")
                
                # Try fresh data as backup
                print("🔄 Trying fresh localhost data...")
                try:
                    from pathlib import Path
                    fresh_data_file = Path(__file__).resolve().parent / 'fresh_localhost_data.json'
                    if fresh_data_file.exists():
                        call_command('loaddata', str(fresh_data_file), verbosity=1)
                        print("✅ Fresh localhost data loaded")
                    else:
                        raise Exception("Fresh localhost data file not found")
                except Exception as fresh_error:
                    print(f"⚠️ Fresh data loading failed: {fresh_error}")
                    
                    # Final fallback to demo content setup
                    print("🔄 Falling back to demo content setup...")
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
print("🔍 FORCE DEPLOY - Environment check:")
print(f"VERCEL env var: {os.environ.get('VERCEL')}")
print(f"VERCEL_URL env var: {os.environ.get('VERCEL_URL')}")
print(f"VERCEL_GIT_COMMIT_SHA: {os.environ.get('VERCEL_GIT_COMMIT_SHA')}")
print(f"LAMBDA_TASK_ROOT: {os.environ.get('LAMBDA_TASK_ROOT')}")
print(f"AWS_LAMBDA_FUNCTION_NAME: {os.environ.get('AWS_LAMBDA_FUNCTION_NAME')}")
print(f"DEPLOYMENT TIMESTAMP: {os.environ.get('VERCEL_DEPLOYMENT_ID', 'Unknown')}")

# Check multiple ways Vercel might be detected
is_vercel = (
    os.environ.get('VERCEL') or 
    os.environ.get('VERCEL_URL') or
    os.environ.get('LAMBDA_TASK_ROOT') or  # Vercel serverless functions
    'vercel' in os.environ.get('HOSTNAME', '').lower() or
    '/var/task' in str(Path(__file__).resolve())  # Vercel lambda path
)

print(f"🎯 IS_VERCEL DETECTED: {is_vercel}")

if is_vercel:
    print("📦 CONFIRMED: Vercel/serverless environment detected")
    print("🚀 Starting database setup process...")
    setup_vercel_database()
    print("✅ Database setup process completed")
else:
    print("🏠 NOT VERCEL: Running in local environment")
    # Even in local, check if we need content for development
    try:
        from core.models import BlogPost
        blog_count = BlogPost.objects.count()
        print(f"📊 Local blog count: {blog_count}")
        if blog_count == 0:
            print("🔧 No content found in local development - running setup...")
            setup_vercel_database()
        else:
            print(f"✅ Content exists locally - {blog_count} blog posts found")
    except Exception as e:
        print(f"🔍 Local content check failed: {e}")
        print("🔧 Running setup anyway due to error...")
        setup_vercel_database()

# Get the WSGI application
application = get_wsgi_application()

# Vercel handler
app = application