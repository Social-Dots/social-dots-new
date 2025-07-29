from pathlib import Path
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-me-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
DEBUG = True # Set to True for development, False for production

# DEBUG = False
print("DEBUG:", DEBUG)

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

ALLOWED_HOSTS = ['*']

# CSRF settings for Vercel deployment
CSRF_TRUSTED_ORIGINS = ['https://*.vercel.app', 'https://*.now.sh', 'https://socialdots.ca', 'https://*.socialdots.ca']
CSRF_COOKIE_SECURE = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'ckeditor',
    'ckeditor_uploader',
    'core',
    'whitenoise',
    'rest_framework',
    'import_export',
    'cloudinary',
    'cloudinary_storage',
]

MIDDLEWARE = [
    # Custom middleware to handle static files in Vercel envi
    # 'core.middleware.ContentSecurityPolicyMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Custom middleware for Content Security Policy
    
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
                'core.context_processors.site_config',
            ],
        },
    },
]

WSGI_APPLICATION = 'socialdots.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Add these at the top of your settings.py
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

# Replace the DATABASES section of your settings.py with this
database_url = os.getenv("DATABASE_URL", "")
tmpPostgres = urlparse(database_url)

# Use SQLite for local development (DISABLED - Using NeonDB for all environments)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# PostgreSQL configuration (NeonDB for all environments)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': tmpPostgres.path.lstrip('/') if tmpPostgres.path else '',
        'USER': tmpPostgres.username,
        'PASSWORD': tmpPostgres.password,
        'HOST': tmpPostgres.hostname,
        'PORT': 5432,
    }
}    



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-ca'

TIME_ZONE = 'America/Toronto'

USE_I18N = True

USE_TZ = True

# Canadian localization
USE_L10N = True
FIRST_DAY_OF_WEEK = 1  # Monday


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# STATIC_URL = '/static/'
# STATIC_ROOT = BASE_DIR / 'staticfiles'

# STATICFILES_DIRS = [
#     BASE_DIR / 'static',
# ]

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Using CompressedStaticFilesStorage instead of CompressedManifestStaticFilesStorage
# to avoid issues with missing manifest entries
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CKEditor Configuration
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
    },
}

# Stripe Configuration
STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')

# Frappe Configuration
FRAPPE_API_URL = os.environ.get('FRAPPE_API_URL')
FRAPPE_API_KEY = os.environ.get('FRAPPE_API_KEY')
FRAPPE_API_SECRET = os.environ.get('FRAPPE_API_SECRET')

# AI Agent Configuration
AI_AGENT_WEBHOOK_URL = os.environ.get('AI_AGENT_WEBHOOK_URL')
AI_AGENT_API_KEY = os.environ.get('AI_AGENT_API_KEY')

# Google Calendar Configuration
GOOGLE_CALENDAR_CLIENT_ID = os.environ.get('GOOGLE_CALENDAR_CLIENT_ID')
GOOGLE_CALENDAR_CLIENT_SECRET = os.environ.get('GOOGLE_CALENDAR_CLIENT_SECRET')
GOOGLE_CALENDAR_REDIRECT_URI = os.environ.get('GOOGLE_CALENDAR_REDIRECT_URI')

# Cloudinary Configuration
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME', 'dsmgydskc'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY', '616489924851549'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET', 'scAYejOSgGs8W8H0QY6LSQ3DjYk'),
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@socialdots.ca')



# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'socialdots.middleware': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# Only create logs directory if not in Vercel environment
if not os.environ.get('VERCEL', False):
    os.makedirs(BASE_DIR / 'logs', exist_ok=True)