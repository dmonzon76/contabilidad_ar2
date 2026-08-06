from django import template
from core.modules import MODULES

register = template.Library()

@register.simple_tag
def get_modules():
    """
    Returns the centralized list of ERP modules.
    """
    return MODULES
