import os

from django import template
from django.conf import settings
from django.templatetags.static import static

register = template.Library()


@register.simple_tag
def static_versioned(path):
    """Appends the file's last-modified timestamp as a cache-busting query
    string, so editing a CSS/JS file during development is reflected
    immediately instead of waiting for the browser's heuristic cache to expire."""
    url = static(path)
    full_path = os.path.join(settings.BASE_DIR, 'static', path)
    try:
        version = int(os.path.getmtime(full_path))
    except OSError:
        version = 0
    return f'{url}?v={version}'
