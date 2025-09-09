from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
from pathlib import Path
import os


class Command(BaseCommand):
    help = 'Complete sync of localhost database to replace all existing data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force complete database reset without confirmation',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🔄 COMPLETE LOCALHOST SYNC - Social Dots Inc.')
        )
        
        if not options['force']:
            confirm = input('⚠️  This will COMPLETELY REPLACE all database content with localhost data. Continue? (yes/no): ')
            if confirm.lower() != 'yes':
                self.stdout.write(self.style.ERROR('❌ Operation cancelled'))
                return

        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        complete_data_file = base_dir / 'complete_localhost_backup.json'

        if not complete_data_file.exists():
            self.stdout.write(
                self.style.ERROR('❌ Complete localhost backup file not found!')
            )
            self.stdout.write(f'Expected file: {complete_data_file}')
            return

        try:
            # Step 1: Flush existing database
            self.stdout.write('🧹 Flushing existing database...')
            call_command('flush', '--noinput', verbosity=1)
            self.stdout.write(self.style.SUCCESS('✅ Database flushed'))

            # Step 2: Run migrations to ensure proper schema
            self.stdout.write('📦 Running migrations...')
            call_command('migrate', verbosity=1)
            self.stdout.write(self.style.SUCCESS('✅ Migrations complete'))

            # Step 3: Load complete localhost data
            self.stdout.write('🔄 Loading complete localhost database...')
            call_command('loaddata', str(complete_data_file), verbosity=1)
            self.stdout.write(self.style.SUCCESS('✅ Localhost data loaded'))

            # Step 4: Verify data
            from core.models import SiteConfiguration, BlogPost, Project, Portfolio, Service, TeamMember
            
            site_config = SiteConfiguration.objects.first()
            blog_count = BlogPost.objects.count()
            project_count = Project.objects.count()
            portfolio_count = Portfolio.objects.count()
            service_count = Service.objects.count()
            team_count = TeamMember.objects.count()

            self.stdout.write('📊 Loaded content verification:')
            self.stdout.write(f'  🏢 Site: {site_config.site_name if site_config else "None"}')
            if site_config:
                self.stdout.write(f'  📧 Contact: {site_config.email}')
                self.stdout.write(f'  📞 Phone: {site_config.phone}')
                self.stdout.write(f'  🎨 Colors: {site_config.primary_color}')
            
            self.stdout.write(f'  📝 Blog Posts: {blog_count}')
            self.stdout.write(f'  🚀 Projects: {project_count}')
            self.stdout.write(f'  🎨 Portfolio: {portfolio_count}')
            self.stdout.write(f'  💼 Services: {service_count}')
            self.stdout.write(f'  👥 Team Members: {team_count}')

            self.stdout.write(
                self.style.SUCCESS('🎉 COMPLETE LOCALHOST SYNC SUCCESSFUL!')
            )
            self.stdout.write('🌐 Your Vercel site should now match localhost exactly!')

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Sync failed: {str(e)}')
            )
            raise e