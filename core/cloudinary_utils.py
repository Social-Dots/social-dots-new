import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary.utils import cloudinary_url
from django.conf import settings

# Cloudinary is already configured in settings.py
# This utility file provides helper functions for working with Cloudinary

def upload_image(image_file, public_id=None, folder='portfolio_images'):
    """
    Upload an image to Cloudinary
    
    Args:
        image_file: The image file to upload
        public_id: Optional public ID for the image
        folder: The folder to upload to (default: portfolio_images)
        
    Returns:
        dict: The Cloudinary upload response
    """
    upload_options = {
        'folder': folder,
        'overwrite': True,
        'resource_type': 'image',
    }
    
    if public_id:
        upload_options['public_id'] = public_id
        
    return cloudinary.uploader.upload(image_file, **upload_options)

def get_optimized_url(public_id, **options):
    """
    Get an optimized URL for an image
    
    Args:
        public_id: The public ID of the image
        **options: Additional options for the URL
        
    Returns:
        str: The optimized URL
    """
    default_options = {
        'fetch_format': 'auto',
        'quality': 'auto',
    }
    
    # Merge default options with provided options
    options = {**default_options, **options}
    
    url, _ = cloudinary_url(public_id, **options)
    return url

def delete_image(public_id):
    """
    Delete an image from Cloudinary
    
    Args:
        public_id: The public ID of the image
        
    Returns:
        dict: The Cloudinary delete response
    """
    return cloudinary.uploader.destroy(public_id)

def create_image_transformation(public_id, **options):
    """
    Create a transformed version of an image
    
    Args:
        public_id: The public ID of the image
        **options: Transformation options
        
    Returns:
        str: The URL of the transformed image
    """
    url, _ = cloudinary_url(public_id, **options)
    return url