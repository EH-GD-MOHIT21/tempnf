from django import template
register = template.Library()

@register.filter('update')
def update(list_obj,value):
    return value in list_obj