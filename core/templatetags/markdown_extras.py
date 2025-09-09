import markdown
import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def markdown_format(text):
    """
    Convert markdown text to HTML
    Usage: {{ content|markdown_format|safe }}
    """
    if not text:
        return ""
    
    # Configure markdown with enhanced extensions for readability
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.fenced_code',
            'markdown.extensions.tables',
            'markdown.extensions.toc',
            'markdown.extensions.codehilite',
            'markdown.extensions.nl2br',
            'markdown.extensions.attr_list',
            'markdown.extensions.def_list',
            'markdown.extensions.footnotes',
            'markdown.extensions.md_in_html',
        ],
        extension_configs={
            'markdown.extensions.codehilite': {
                'css_class': 'highlight',
                'use_pygments': True,
                'noclasses': False,
            }
        }
    )
    
    html = md.convert(text)
    return mark_safe(html)

@register.filter
def blog_content_format(text):
    """
    Convert markdown text to HTML for blog posts, removing the first H1 if present
    and improving the structure for better readability
    """
    if not text:
        return ""
    
    # Remove the first H1 heading from markdown since we show title separately
    text_lines = text.split('\n')
    if text_lines and text_lines[0].startswith('# '):
        # Remove the first H1 line and any following empty lines
        text_lines = text_lines[1:]
        while text_lines and text_lines[0].strip() == '':
            text_lines.pop(0)
        text = '\n'.join(text_lines)
    
    # Configure markdown with enhanced extensions
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.fenced_code',
            'markdown.extensions.tables',
            'markdown.extensions.toc',
            'markdown.extensions.codehilite',
            'markdown.extensions.nl2br',
            'markdown.extensions.attr_list',
            'markdown.extensions.def_list',
            'markdown.extensions.footnotes',
            'markdown.extensions.md_in_html',
        ],
        extension_configs={
            'markdown.extensions.codehilite': {
                'css_class': 'highlight',
                'use_pygments': True,
                'noclasses': False,
            }
        }
    )
    
    html = md.convert(text)
    
    # Add some additional formatting improvements
    # Add classes to elements for better styling
    html = re.sub(r'<h2([^>]*)>', r'<h2\1 class="section-heading">', html)
    html = re.sub(r'<h3([^>]*)>', r'<h3\1 class="subsection-heading">', html)
    html = re.sub(r'<p([^>]*)>', r'<p\1 class="content-paragraph">', html)
    html = re.sub(r'<ul([^>]*)>', r'<ul\1 class="content-list">', html)
    html = re.sub(r'<ol([^>]*)>', r'<ol\1 class="content-list numbered">', html)
    
    return mark_safe(html)

# Also provide a shorter alias
register.filter('markdown', markdown_format)