from django.core.management.base import BaseCommand
from django.core.management import call_command
from pathlib import Path


class Command(BaseCommand):
    help = 'Deploy complete localhost to Vercel with all data and assets'

    def handle(self, *args, **options):
        try:
            base_dir = Path(__file__).resolve().parent.parent.parent.parent
            
            # Load complete localhost data
            core_data_file = base_dir / 'complete_working_localhost.json'
            users_data_file = base_dir / 'complete_working_users.json'
            
            self.stdout.write('Loading complete localhost data...')
            
            if users_data_file.exists():
                call_command('loaddata', str(users_data_file), verbosity=1)
                self.stdout.write('Users loaded')
                
            if core_data_file.exists():
                call_command('loaddata', str(core_data_file), verbosity=1)
                self.stdout.write('Core data loaded')
            
            # Verify data loaded correctly
            from core.models import SiteConfiguration, Service, Project, BlogPost, TeamMember
            
            site_config = SiteConfiguration.objects.first()
            self.stdout.write(f'Site: {site_config.site_name if site_config else "None"}')
            self.stdout.write(f'Services: {Service.objects.count()}')
            self.stdout.write(f'Projects: {Project.objects.count()}') 
            self.stdout.write(f'Blog Posts: {BlogPost.objects.count()}')
            self.stdout.write(f'Team Members: {TeamMember.objects.count()}')
            
            self.stdout.write('Complete localhost deployment successful!')
            
        except Exception as e:
            self.stdout.write(f'Error: {str(e)}')
            raise e