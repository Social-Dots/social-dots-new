from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User
import json
import os
from pathlib import Path


class Command(BaseCommand):
    help = 'Load production data from localhost exports'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Loading production data from localhost...')
        )

        base_dir = Path(__file__).resolve().parent.parent.parent.parent

        # Load users first
        users_file = base_dir / 'localhost_users.json'
        if users_file.exists():
            self.stdout.write('👤 Loading users...')
            call_command('loaddata', str(users_file), verbosity=1)
            self.stdout.write(self.style.SUCCESS('✅ Users loaded'))
        else:
            self.stdout.write(self.style.WARNING('⚠️ Users file not found, skipping'))

        # Load core data
        data_file = base_dir / 'localhost_data.json'
        if data_file.exists():
            self.stdout.write('📦 Loading core application data...')
            call_command('loaddata', str(data_file), verbosity=1)
            self.stdout.write(self.style.SUCCESS('✅ Core data loaded'))
        else:
            self.stdout.write(self.style.ERROR('❌ Production data file not found!'))
            return

        # Verify data was loaded
        from core.models import SiteConfiguration, BlogPost, Project, Portfolio, Service

        site_config = SiteConfiguration.objects.first()
        blog_count = BlogPost.objects.count()
        project_count = Project.objects.count()
        portfolio_count = Portfolio.objects.count()
        service_count = Service.objects.count()

        self.stdout.write(f'📊 Content loaded:')
        self.stdout.write(f'  - Site: {site_config.site_name if site_config else "None"}')
        self.stdout.write(f'  - Blogs: {blog_count}')
        self.stdout.write(f'  - Projects: {project_count}')
        self.stdout.write(f'  - Portfolio: {portfolio_count}')
        self.stdout.write(f'  - Services: {service_count}')

        self.stdout.write(
            self.style.SUCCESS('🎉 Production data loaded successfully!')
        )