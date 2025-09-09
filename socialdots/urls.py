
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

# Add emergency routes as backup (lower priority)
if EMERGENCY_MODE:
    urlpatterns += [
        path('emergency/health/', emergency_health, name='emergency_health'),
        path('emergency/test/', emergency_test, name='emergency_test'), 
        path('emergency/', emergency_home, name='emergency_home'),
    ]

# Main website URLs
try:
    # Import sitemaps and add full functionality
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
        path('', include('core.urls')),  # Main website URLs
    ]
    
except Exception as e:
    # If core URLs fail, provide emergency fallback
    if EMERGENCY_MODE:
        urlpatterns += [
            path('', emergency_home, name='emergency_fallback'),
        ]

# Serve media files in both development and production
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
