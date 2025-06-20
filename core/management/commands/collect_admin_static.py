import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib import admin

class Command(BaseCommand):
    help = 'Explicitly collects admin static files to ensure they are available in production'

    def handle(self, *args, **options):
        # Get the path to the admin static files
        admin_static_path = os.path.join(os.path.dirname(admin.__file__), 'static', 'admin')
        
        # Get the destination path
        dest_path = os.path.join(settings.STATIC_ROOT, 'admin')
        
        # Create the destination directory if it doesn't exist
        os.makedirs(dest_path, exist_ok=True)
        
        # Copy the admin static files
        self.stdout.write(f'Copying admin static files from {admin_static_path} to {dest_path}')
        
        # Walk through the admin static directory and copy all files
        for root, dirs, files in os.walk(admin_static_path):
            for file in files:
                src_file = os.path.join(root, file)
                # Get the relative path from the admin static directory
                rel_path = os.path.relpath(src_file, admin_static_path)
                # Create the destination path
                dst_file = os.path.join(dest_path, rel_path)
                # Create the destination directory if it doesn't exist
                os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                # Copy the file
                shutil.copy2(src_file, dst_file)
                self.stdout.write(f'Copied {rel_path}')
        
        self.stdout.write(self.style.SUCCESS('Successfully collected admin static files'))