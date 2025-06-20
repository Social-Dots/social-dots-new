import logging
import os
from django.conf import settings
from django.http import HttpResponseRedirect, FileResponse
from django.contrib.staticfiles import finders

# Set up logger
logger = logging.getLogger('socialdots.middleware')

class HttpsRedirectMiddleware:
    """
    Middleware to handle HTTPS requests in development environment.
    Redirects HTTPS requests to HTTP when in development mode.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        logger.info('HttpsRedirectMiddleware initialized')

    def __call__(self, request):
        # Only apply in development mode
        if settings.DEBUG and request.is_secure():
            # If the request is HTTPS, redirect to HTTP
            url = request.build_absolute_uri(request.get_full_path())
            url = url.replace('https://', 'http://')
            logger.debug(f'Redirecting HTTPS request to HTTP: {url}')
            return HttpResponseRedirect(url)
        
        return self.get_response(request)


class StaticFilesMiddleware:
    """
    Middleware to handle static files in Vercel environment.
    Helps serve admin static files when the manifest is missing.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        logger.info('StaticFilesMiddleware initialized')
        # Initialize admin static files path
        self.admin_static_path = None
        try:
            import django.contrib.admin as admin_module
            self.admin_static_path = os.path.join(os.path.dirname(admin_module.__file__), 'static', 'admin')
            logger.info(f'Admin static files path: {self.admin_static_path}')
        except Exception as e:
            logger.error(f'Error initializing admin static path: {str(e)}')

    def __call__(self, request):
        # Check if the request is for a static file
        if request.path.startswith(settings.STATIC_URL):
            # Extract the relative path from the URL
            relative_path = request.path[len(settings.STATIC_URL):]
            
            # Log the requested static file
            logger.debug(f'Static file requested: {relative_path}')
            
            # First try to find the file using Django's finders
            file_path = finders.find(relative_path)
            
            if file_path:
                logger.debug(f'Serving static file from finder: {file_path}')
                return FileResponse(open(file_path, 'rb'))
            
            # Special handling for admin files
            if relative_path.startswith('admin/') and self.admin_static_path:
                # Get the path relative to the admin directory
                admin_relative_path = relative_path[6:]  # Remove 'admin/' prefix
                admin_file_path = os.path.join(self.admin_static_path, admin_relative_path)
                
                if os.path.exists(admin_file_path) and os.path.isfile(admin_file_path):
                    logger.debug(f'Serving admin static file directly: {admin_file_path}')
                    return FileResponse(open(admin_file_path, 'rb'))
            
            # Check in STATIC_ROOT as a last resort
            static_root_path = os.path.join(settings.STATIC_ROOT, relative_path)
            if os.path.exists(static_root_path) and os.path.isfile(static_root_path):
                logger.debug(f'Serving static file from STATIC_ROOT: {static_root_path}')
                return FileResponse(open(static_root_path, 'rb'))
            
            # Special handling for Vercel environment
            if os.environ.get('VERCEL'):
                # Try all possible static file locations in Vercel environment
                possible_paths = [
                    # /tmp/staticfiles (our configured STATIC_ROOT in Vercel)
                    os.path.join('/tmp/staticfiles', relative_path),
                    # /var/task/staticfiles (default location Vercel might look for)
                    os.path.join('/var/task/staticfiles', relative_path),
                    # /var/task/static (another possible location)
                    os.path.join('/var/task/static', relative_path),
                    # Root level static directory
                    os.path.join('/var/task', 'static', relative_path),
                    # Try with 'static' prefix removed if it exists in the path
                    os.path.join('/var/task', relative_path)
                ]
                
                # Special handling for admin files - try additional paths
                if relative_path.startswith('admin/'):
                    admin_relative_path = relative_path[6:]  # Remove 'admin/' prefix
                    possible_paths.extend([
                        # Direct admin path in tmp
                        os.path.join('/tmp/staticfiles/admin', admin_relative_path),
                        # Direct admin path in var/task
                        os.path.join('/var/task/staticfiles/admin', admin_relative_path),
                        # Direct admin path in var/task/static
                        os.path.join('/var/task/static/admin', admin_relative_path)
                    ])
                
                # Try each path
                for path in possible_paths:
                    if os.path.exists(path) and os.path.isfile(path):
                        logger.info(f'Serving static file from Vercel path: {path}')
                        return FileResponse(open(path, 'rb'))
                
                # Log all possible locations we've checked
                logger.warning(f'Static file not found in any location: {relative_path}')
                logger.warning(f'Checked paths: finder, admin_static_path, {static_root_path}, and:')
                for path in possible_paths:
                    logger.warning(f'  - {path}')
                
                # Try to list directories to help with debugging
                try:
                    if os.path.exists('/var/task'):
                        logger.info(f'/var/task directory exists, contents: {os.listdir("/var/task")}')
                    if os.path.exists('/var/task/staticfiles'):
                        logger.info(f'/var/task/staticfiles directory exists, contents: {os.listdir("/var/task/staticfiles")}')
                    if os.path.exists('/tmp/staticfiles'):
                        logger.info(f'/tmp/staticfiles directory exists, contents: {os.listdir("/tmp/staticfiles")}')
                except Exception as e:
                    logger.error(f'Error listing directories: {str(e)}')
            else:
                logger.warning(f'Static file not found: {relative_path}')
        
        # If not a static file or file not found, continue with normal processing
        return self.get_response(request)