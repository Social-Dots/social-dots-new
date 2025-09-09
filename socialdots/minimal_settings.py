"""
Minimal Django settings for emergency deployment
Removes all problematic apps and dependencies
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-minimal-emergency-key')
DEBUG = False
ALLOWED_HOSTS = ['*']

# Minimal INSTALLED_APPS - Django core + essential dependencies
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth', 
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # Required by core views
    'core',  # Our main app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', 
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'socialdots.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request', 
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'socialdots.wsgi.application'

# SQLite for emergency deployment
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files configuration for Vercel
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Use whitenoise for static file serving
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Media files  
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Service configurations (minimal/mock values for emergency deployment)
STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY', 'mock_stripe_public_key')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', 'mock_stripe_secret_key')
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET', 'mock_webhook_secret')

# Frappe Configuration (mock values)
FRAPPE_API_URL = os.environ.get('FRAPPE_API_URL', 'https://mock.frappe.local')
FRAPPE_API_KEY = os.environ.get('FRAPPE_API_KEY', 'mock_frappe_key')
FRAPPE_API_SECRET = os.environ.get('FRAPPE_API_SECRET', 'mock_frappe_secret')

# AI Agent Configuration (mock values)
AI_AGENT_WEBHOOK_URL = os.environ.get('AI_AGENT_WEBHOOK_URL', 'https://mock.ai.local')
AI_AGENT_API_KEY = os.environ.get('AI_AGENT_API_KEY', 'mock_ai_key')

# Slack Configuration (mock values)
SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL', 'https://mock.slack.local')
SLACK_CHANNEL = os.environ.get('SLACK_CHANNEL', '#mock-notifications')

# Google Calendar Configuration (mock values)
GOOGLE_CALENDAR_CLIENT_ID = os.environ.get('GOOGLE_CALENDAR_CLIENT_ID', 'mock_client_id')
GOOGLE_CALENDAR_CLIENT_SECRET = os.environ.get('GOOGLE_CALENDAR_CLIENT_SECRET', 'mock_secret')
GOOGLE_CALENDAR_REDIRECT_URI = os.environ.get('GOOGLE_CALENDAR_REDIRECT_URI', 'https://mock.calendar.local')

# Email Configuration (mock values)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Console backend for testing
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.mock.local')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'mock@example.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'mock_password')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@socialdots.ca')

print("MINIMAL SETTINGS LOADED - Emergency deployment mode active")
print(f"STRIPE_SECRET_KEY configured: {'Yes' if STRIPE_SECRET_KEY != 'mock_stripe_secret_key' else 'No (using mock)'}")