from django import template

register = template.Library()

# 定义一个过滤器
@register.filter
def add_hello(value, arg):
    return '{}_hello_{}'.format(value, arg)

# 定义sample_tag
@register.simple_tag
def str_join(*args,**kwargs):
    return '{}__{}'.format('--'.join(args),'++++'.join(kwargs.values()))

@register.inclusion_tag('li.html')
def show_li(num):
    return {'number':range(num)}