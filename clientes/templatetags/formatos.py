from django import template
register = template.Library()

@register.filter(name='formato_clp')
def formato_clp(value):
    return "${:,.0f}".format(value).replace(',', '.')