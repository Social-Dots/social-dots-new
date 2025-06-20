import os
import shutil
import logging
from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.finders import get_finder
from django.contrib.staticfiles.storage import staticfiles_storage

# Set up logger
logger = logging.getLogger('django.management.commands')

class Command(BaseCommand):
    help = 'Explicitly collects admin static files to ensure they are available in production'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force copying of admin static files even if they already exist',
        )

    def handle(self, *args, **options):
        verbosity = options.get('verbosity', 1)
        force = options.get('force', False)
        
        # Get the path to the admin static files
        admin_static_path = os.path.join(os.path.dirname(admin.__file__), 'static', 'admin')
        
        # Get the destination path
        dest_path = os.path.join(settings.STATIC_ROOT, 'admin')
        
        # Create the destination directory if it doesn't exist
        os.makedirs(dest_path, exist_ok=True)
        
        self.stdout.write(f'Copying admin static files from {admin_static_path} to {dest_path}')
        
        # Track statistics
        copied_files = 0
        skipped_files = 0
        error_files = 0
        
        # Walk through the admin static directory and copy all files
        for root, dirs, files in os.walk(admin_static_path):
            for file in files:
                try:
                    src_file = os.path.join(root, file)
                    # Get the relative path from the admin static directory
                    rel_path = os.path.relpath(src_file, admin_static_path)
                    # Create the destination path
                    dst_file = os.path.join(dest_path, rel_path)
                    
                    # Check if file already exists and skip if not forced
                    if os.path.exists(dst_file) and not force:
                        if verbosity >= 2:
                            self.stdout.write(f'Skipping existing file: {rel_path}')
                        skipped_files += 1
                        continue
                    
                    # Create the destination directory if it doesn't exist
                    os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                    
                    # Copy the file
                    shutil.copy2(src_file, dst_file)
                    copied_files += 1
                    
                    if verbosity >= 2:
                        self.stdout.write(f'Copied {rel_path}')
                except Exception as e:
                    error_files += 1
                    self.stderr.write(f'Error copying {file}: {str(e)}')
        
        # Try to also collect admin static files using Django's finders
        try:
            self.stdout.write('Attempting to collect admin static files using Django finders...')
            from django.contrib.staticfiles.finders import AppDirectoriesFinder
            finder = AppDirectoriesFinder()
            for path, storage in finder.list(['admin']):
                try:
                    # Get the source file path
                    src_file = storage.path(path)
                    # Create the destination path
                    dst_file = os.path.join(settings.STATIC_ROOT, path)
                    
                    # Check if file already exists and skip if not forced
                    if os.path.exists(dst_file) and not force:
                        if verbosity >= 2:
                            self.stdout.write(f'Skipping existing file: {path}')
                        skipped_files += 1
                        continue
                    
                    # Create the destination directory if it doesn't exist
                    os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                    
                    # Copy the file
                    shutil.copy2(src_file, dst_file)
                    copied_files += 1
                    
                    if verbosity >= 2:
                        self.stdout.write(f'Copied {path} using finder')
                except Exception as e:
                    error_files += 1
                    self.stderr.write(f'Error copying {path} using finder: {str(e)}')
        except Exception as e:
            self.stderr.write(f'Error using Django finders: {str(e)}')
        
        # Summary
        self.stdout.write(self.style.SUCCESS(
            f'Admin static files collection complete: '
            f'{copied_files} files copied, {skipped_files} files skipped, {error_files} errors'
        ))