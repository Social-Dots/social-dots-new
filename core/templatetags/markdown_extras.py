import markdown
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
    
    # Configure markdown with extensions for proper heading conversion
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.fenced_code',
            'markdown.extensions.tables',
            'markdown.extensions.toc',
            'markdown.extensions.codehilite',
        ],
        extension_configs={
            'markdown.extensions.codehilite': {
                'css_class': 'highlight'
            }
        }
    )
    
    html = md.convert(text)
    return mark_safe(html)

# Also provide a shorter alias
register.filter('markdown', markdown_format)