from django import template
from django.contrib import admin

register = template.Library()

@register.simple_tag
def admin_site_url():
    if admin.site.has_permission(None):
        return '/admin/'  # Provide the URL of your admin site
    return '/'  # Provide the URL of your normal site
