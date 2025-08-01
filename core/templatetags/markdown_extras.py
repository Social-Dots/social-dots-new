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

# Also provide a shorter alias
register.filter('markdown', markdown_format)