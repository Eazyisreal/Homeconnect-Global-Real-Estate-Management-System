from django import template

register = template.Library()

@register.filter(name='format_int_with_commas')
def format_int_with_commas(value):
    return "{:,}".format(value)

@register.filter(name='format_features')
def format_features(features):
    return ' | '.join(features.split(','))