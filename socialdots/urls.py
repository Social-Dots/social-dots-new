
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Emergency views disabled for production
EMERGENCY_MODE = False

urlpatterns = [
    path('admin/', admin.site.urls),
]

# Emergency routes disabled

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
    # If core URLs fail, add a simple fallback
    from django.http import HttpResponse
    def simple_fallback(request):
        return HttpResponse("Social Dots Inc. - Site temporarily unavailable")

    urlpatterns += [
        path('', simple_fallback, name='emergency_fallback'),
    ]

# Serve media files in both development and production
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
