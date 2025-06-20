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

    def __call__(self, request):
        # Check if the request is for a static file
        if request.path.startswith(settings.STATIC_URL):
            # Extract the relative path from the URL
            relative_path = request.path[len(settings.STATIC_URL):]
            
            # Try to find the file using Django's finders
            file_path = finders.find(relative_path)
            
            if file_path:
                logger.debug(f'Serving static file: {file_path}')
                return FileResponse(open(file_path, 'rb'))
        
        # If not a static file or file not found, continue with normal processing
        return self.get_response(request)