from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Service, Portfolio, BlogPost, Project


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['home', 'services', 'portfolio', 'blog', 'about', 'contact']

    def location(self, item):
        return reverse(item)


class ServiceSitemap(Sitemap):
    priority = 0.7
    changefreq = 'monthly'

    def items(self):
        return Service.objects.filter(is_active=True)

    def location(self, obj):
        return reverse('service_detail', args=[obj.slug])

    def lastmod(self, obj):
        return obj.updated_at


class PortfolioSitemap(Sitemap):
    priority = 0.7
    changefreq = 'monthly'

    def items(self):
        return Portfolio.objects.filter(is_active=True)

    def location(self, obj):
        return reverse('portfolio_detail', args=[obj.slug])

    def lastmod(self, obj):
        return obj.updated_at


class ProjectSitemap(Sitemap):
    priority = 0.6
    changefreq = 'monthly'

    def items(self):
        return Project.objects.filter(is_active=True)

    def location(self, obj):
        return reverse('project_detail', args=[obj.slug])

    def lastmod(self, obj):
        return obj.updated_at


class BlogSitemap(Sitemap):
    priority = 0.6
    changefreq = 'weekly'

    def items(self):
        return BlogPost.objects.filter(status='published')

    def location(self, obj):
        return reverse('blog_detail', args=[obj.slug])

    def lastmod(self, obj):
        return obj.updated_at