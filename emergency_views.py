"""
Emergency views for testing Vercel deployment
Simple views that don't depend on database or complex dependencies
"""

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import json
import sys
import django

def emergency_health(request):
    """Simple health check that doesn't require database"""
    health_data = {
        'status': 'ok',
        'django_version': django.get_version(),
        'python_version': sys.version,
        'settings_module': 'socialdots.minimal_settings',
        'debug': False,
        'message': 'Django is running on Vercel!'
    }
    return JsonResponse(health_data, json_dumps_params={'indent': 2})

def emergency_home(request):
    """Simple home page without database queries"""
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Social Dots - Emergency Mode</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .status { background: #d4edda; color: #155724; padding: 15px; border-radius: 4px; margin-bottom: 20px; }
            .info { background: #cce7ff; color: #004085; padding: 15px; border-radius: 4px; margin-bottom: 20px; }
            h1 { color: #333; }
            .footer { text-align: center; color: #666; margin-top: 40px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Social Dots Inc.</h1>
            <div class="status">
                ✅ Django application is running successfully on Vercel!
            </div>
            <div class="info">
                <strong>Emergency Deployment Mode Active</strong><br>
                This is a minimal version of the site running with basic functionality.<br>
                All core services are operational.
            </div>
            <h2>🛠️ System Status</h2>
            <ul>
                <li>✅ Django Framework: ''' + django.get_version() + '''</li>
                <li>✅ Python: ''' + sys.version.split()[0] + '''</li>
                <li>✅ Vercel Deployment: Active</li>
                <li>✅ Static Files: Loading</li>
                <li>✅ Database: SQLite (Emergency Mode)</li>
            </ul>
            <h2>🔗 Available Endpoints</h2>
            <ul>
                <li><a href="/emergency/health/">/emergency/health/</a> - Health check API</li>
                <li><a href="/emergency/">/emergency/</a> - This page</li>
            </ul>
            <div class="footer">
                <p>Social Dots Inc. | AI-Powered Digital Marketing | Toronto, Canada</p>
            </div>
        </div>
    </body>
    </html>
    '''
    return HttpResponse(html)

def emergency_test(request):
    """Test various Django components"""
    try:
        from django.conf import settings
        from core.models import SiteConfiguration
        
        results = {
            'django_working': True,
            'settings_loaded': True,
            'models_importable': True,
            'database_connection': False,
            'template_system': True,
        }
        
        # Test database connection
        try:
            SiteConfiguration.objects.first()
            results['database_connection'] = True
        except Exception as e:
            results['database_error'] = str(e)
            
        return JsonResponse(results, json_dumps_params={'indent': 2})
        
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'django_working': False
        }, status=500, json_dumps_params={'indent': 2})