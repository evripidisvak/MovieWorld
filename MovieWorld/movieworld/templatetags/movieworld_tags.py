from django import template

# from django.template import resolve_variable

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, field, value):
    dict_ = context["request"].GET.copy()
    dict_[field] = value
    return dict_.urlencode()
