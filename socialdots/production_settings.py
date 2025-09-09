"""
Production-specific Django settings
Overrides base settings for Vercel deployment
"""

from .settings import *

# Remove problematic apps for Vercel deployment
INSTALLED_APPS = [app for app in INSTALLED_APPS if app != 'markdownify']

# Add debugging for production
print("PRODUCTION SETTINGS LOADED - markdownify removed from INSTALLED_APPS")
print(f"INSTALLED_APPS: {INSTALLED_APPS}")