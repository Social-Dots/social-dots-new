
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Emergency views for minimal deployment
try:
    from emergency_views import emergency_health, emergency_home, emergency_test
    EMERGENCY_MODE = True
except ImportError:
    EMERGENCY_MODE = False

urlpatterns = [
    path('admin/', admin.site.urls),
]

# Emergency routes (high priority)
if EMERGENCY_MODE:
    urlpatterns += [
        path('emergency/health/', emergency_health, name='emergency_health'),
        path('emergency/test/', emergency_test, name='emergency_test'), 
        path('emergency/', emergency_home, name='emergency_home'),
        path('', emergency_home, name='home'),  # Emergency home as default
    ]

# Try to include core URLs with error handling
try:
    if not EMERGENCY_MODE:
        # Import complex dependencies only if not in emergency mode
        from django.contrib.sitemaps.views import sitemap
        from core.sitemap import StaticViewSitemap, ServiceSitemap, PortfolioSitemap, ProjectSitemap, BlogSitemap
        
        sitemaps = {
            'static': StaticViewSitemap,
            'services': ServiceSitemap,
            'portfolio': PortfolioSitemap,
            'projects': ProjectSitemap,
            'blog': BlogSitemap,
        }
        
        urlpatterns += [
            path('ckeditor/', include('ckeditor_uploader.urls')),
            path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
            path('', include('core.urls')),
        ]
    else:
        # Add core URLs under /core/ prefix in emergency mode
        urlpatterns += [
            path('core/', include('core.urls')),
        ]
        
except Exception as e:
    # If anything fails, emergency mode will handle all routing
    pass

# Serve media files in both development and production
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
