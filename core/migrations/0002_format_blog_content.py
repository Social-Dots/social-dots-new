from django.db import migrations
import re

def format_blog_content(apps, schema_editor):
    BlogPost = apps.get_model('core', 'BlogPost')
    
    def add_inline_styles(content):
        if not content:
            return content
        
        # Add inline styles to H1 elements
        content = re.sub(
            r'<h1([^>]*)>',
            r'<h1\1 style="font-size: 2.5rem !important; background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%) !important; border: 3px solid #1e40af !important; padding: 1.5rem 2rem !important; margin: 2rem 0 !important; border-radius: 12px !important; box-shadow: 0 8px 25px rgba(30, 64, 175, 0.15) !important; font-weight: 700 !important; color: #1e40af !important; line-height: 1.2 !important;">',
            content
        )
        
        # Add inline styles to H2 elements
        content = re.sub(
            r'<h2([^>]*)>',
            r'<h2\1 style="font-size: 2rem !important; background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%) !important; border: 2px solid #3b82f6 !important; padding: 1.25rem 1.75rem !important; margin: 1.75rem 0 1.25rem 0 !important; border-radius: 10px !important; box-shadow: 0 6px 20px rgba(59, 130, 246, 0.12) !important; font-weight: 600 !important; color: #1e40af !important; line-height: 1.3 !important;">',
            content
        )
        
        # Add inline styles to H3 elements
        content = re.sub(
            r'<h3([^>]*)>',
            r'<h3\1 style="font-size: 1.5rem !important; background: linear-gradient(135deg, #fed7aa 0%, #fdba74 100%) !important; border: 2px solid #ea580c !important; padding: 1rem 1.5rem !important; margin: 1.5rem 0 1rem 0 !important; border-radius: 8px !important; box-shadow: 0 4px 15px rgba(234, 88, 12, 0.1) !important; font-weight: 600 !important; color: #c2410c !important; line-height: 1.4 !important;">',
            content
        )
        
        # Add inline styles to P elements
        content = re.sub(
            r'<p([^>]*)>',
            r'<p\1 style="background: rgba(254, 215, 170, 0.1) !important; padding: 1rem 1.25rem !important; margin: 1rem 0 !important; border-radius: 6px !important; border-left: 4px solid #f97316 !important; box-shadow: 0 2px 8px rgba(249, 115, 22, 0.05) !important; line-height: 1.7 !important; font-size: 1.1rem !important; color: #374151 !important;">',
            content
        )
        
        # Add inline styles to UL elements
        content = re.sub(
            r'<ul([^>]*)>',
            r'<ul\1 style="background: rgba(220, 252, 231, 0.3) !important; border: 1px solid #10b981 !important; border-radius: 8px !important; padding: 1.25rem 1.5rem !important; margin: 1.25rem 0 !important; box-shadow: 0 3px 12px rgba(16, 185, 129, 0.08) !important; list-style-type: disc !important; padding-left: 2.5rem !important;">',
            content
        )
        
        # Add inline styles to OL elements
        content = re.sub(
            r'<ol([^>]*)>',
            r'<ol\1 style="background: rgba(220, 252, 231, 0.3) !important; border: 1px solid #10b981 !important; border-radius: 8px !important; padding: 1.25rem 1.5rem !important; margin: 1.25rem 0 !important; box-shadow: 0 3px 12px rgba(16, 185, 129, 0.08) !important; list-style-type: decimal !important; padding-left: 2.5rem !important;">',
            content
        )
        
        return content
    
    for post in BlogPost.objects.all():
        if post.content:
            formatted_content = add_inline_styles(post.content)
            if formatted_content != post.content:
                post.content = formatted_content
                post.save()

def reverse_format_blog_content(apps, schema_editor):
    # Reverse operation - remove inline styles
    BlogPost = apps.get_model('core', 'BlogPost')
    
    for post in BlogPost.objects.all():
        if post.content:
            # Remove style attributes
            content = re.sub(r' style="[^"]*"', '', post.content)
            post.content = content
            post.save()

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(format_blog_content, reverse_format_blog_content),
    ]