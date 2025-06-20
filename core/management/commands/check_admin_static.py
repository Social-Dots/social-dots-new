import os
import requests
import logging
from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.staticfiles import finders

# Set up logger
logger = logging.getLogger('django.management.commands')

class Command(BaseCommand):
    help = 'Check if admin static files are accessible and properly configured'

    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            type=str,
            help='Base URL to check (e.g., http://localhost:8000 or https://your-app.vercel.app)',
            required=True
        )

    def handle(self, *args, **options):
        base_url = options['url'].rstrip('/')
        self.stdout.write(f'Checking admin static files at {base_url}')
        
        # List of critical admin static files to check
        critical_files = [
            '/static/admin/css/base.css',
            '/static/admin/css/login.css',
            '/static/admin/js/core.js',
            '/static/admin/img/icon-yes.svg',
        ]
        
        success_count = 0
        failure_count = 0
        
        for file_path in critical_files:
            url = f'{base_url}{file_path}'
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    self.stdout.write(self.style.SUCCESS(f'✓ {file_path} - OK'))
                    success_count += 1
                else:
                    self.stdout.write(self.style.ERROR(f'✗ {file_path} - Failed with status code {response.status_code}'))
                    failure_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ {file_path} - Error: {str(e)}'))
                failure_count += 1
        
        # Check if files exist in STATIC_ROOT
        self.stdout.write('\nChecking files in STATIC_ROOT:')
        for file_path in critical_files:
            # Remove /static/ prefix
            relative_path = file_path[8:]
            full_path = os.path.join(settings.STATIC_ROOT, relative_path)
            if os.path.exists(full_path):
                self.stdout.write(self.style.SUCCESS(f'✓ {full_path} - Exists'))
            else:
                self.stdout.write(self.style.ERROR(f'✗ {full_path} - Not found'))
        
        # Check if files can be found by Django's finders
        self.stdout.write('\nChecking files with Django finders:')
        for file_path in critical_files:
            # Remove /static/ prefix
            relative_path = file_path[8:]
            found_path = finders.find(relative_path)
            if found_path:
                self.stdout.write(self.style.SUCCESS(f'✓ {relative_path} - Found at {found_path}'))
            else:
                self.stdout.write(self.style.ERROR(f'✗ {relative_path} - Not found by finders'))
        
        # Summary
        self.stdout.write('\nSummary:')
        self.stdout.write(f'Total files checked: {len(critical_files)}')
        self.stdout.write(self.style.SUCCESS(f'Successful: {success_count}'))
        self.stdout.write(self.style.ERROR(f'Failed: {failure_count}'))
        
        if failure_count == 0:
            self.stdout.write(self.style.SUCCESS('\nAll admin static files are accessible!'))
        else:
            self.stdout.write(self.style.ERROR(f'\n{failure_count} admin static files are not accessible.'))
            self.stdout.write('Suggestions:')
            self.stdout.write('1. Check if STATIC_ROOT is correctly configured')
            self.stdout.write('2. Ensure collectstatic command is running successfully')
            self.stdout.write('3. Verify that the StaticFilesMiddleware is properly configured')
            self.stdout.write('4. Check Vercel routes configuration in vercel.json')