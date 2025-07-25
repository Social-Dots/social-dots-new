import logging

logger = logging.getLogger(__name__)

class ContentSecurityPolicyMiddleware:
    """
    Middleware to add Content Security Policy headers to responses.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Add CSP header to allow Google Calendar API scripts
        csp_directives = {
            # Allow scripts from these sources
            'script-src': [
                "'self'", "'unsafe-inline'", "'unsafe-eval'", "blob:", "data:",
                "https://www.google.com", "https://*.google.com", 
                "https://apis.google.com", "https://*.googleapis.com",
                "https://www.gstatic.com", "https://*.gstatic.com",
                "https://calendar-pa.clients6.google.com",
                "https://calendar.google.com",
                "https://accounts.google.com",
                "https://apis.google.com/js/api.js",
                "https://apis.google.com/js/client.js",
                "https://apis.google.com/_/scs/abc-static/_/js/",
                "https://www.gstatic.com/_/mss/boq-calendar/_/js/",
                "https://www.gstatic.com/recaptcha/releases/"
            ],
            # Allow frames from these sources
            'frame-src': [
                "'self'", "https://calendar.google.com", "https://*.google.com",
                "https://calendar-pa.clients6.google.com", "https://accounts.google.com",
                "https://appointments.googleapis.com"
            ],
            # Allow connections to these sources
            'connect-src': [
                "'self'", "https://apis.google.com", "https://*.googleapis.com",
                "https://calendar-pa.clients6.google.com", "https://*.google.com",
                "https://accounts.google.com", "https://appointments.googleapis.com",
                "https://calendar-pa.clients6.google.com/$rpc/google.internal.calendar.v1.AppointmentBookingService/*",
                "https://calendar-pa.clients6.google.com/$rpc/*"
            ],
            # Allow images from these sources
            'img-src': [
                "'self'", "data:", "https://*.google.com", "https://*.gstatic.com",
                "https://calendar-pa.clients6.google.com", "https://*.googleapis.com"
            ],
            # Allow styles from these sources
            'style-src': [
                "'self'", "'unsafe-inline'", "https://*.google.com", "https://*.gstatic.com",
                "https://*.googleapis.com"
            ],
            # Allow fonts from these sources
            'font-src': [
                "'self'", "data:", "https://*.gstatic.com", "https://fonts.googleapis.com",
                "https://fonts.gstatic.com"
            ],
            # Allow objects from these sources
            'object-src': ["'none'"],
            # Allow frames to be embedded in these sources
            'frame-ancestors': ["'self'", "https://calendar.google.com", "https://*.google.com"]
        }
        
        # Build the CSP header value
        csp_value = ''
        for directive, sources in csp_directives.items():
            if sources:
                csp_value += directive + ' ' + ' '.join(sources) + '; '
        
        # Set the CSP header
        response['Content-Security-Policy'] = csp_value
        
        # Also set the Report-Only version for debugging if needed
        # response['Content-Security-Policy-Report-Only'] = csp_value
        
        return response