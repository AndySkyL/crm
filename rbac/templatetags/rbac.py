from django.template import Library
from django.conf import settings
from collections import OrderedDict


register = Library()


@register.inclusion_tag('menu.html')
def menu(request):
    menus_dict = request.session[settings.MENU_SESSION_KEY]
    order_dict = OrderedDict()

    for key in sorted(menus_dict,key=lambda x:menus_dict[x]['weight'],reverse=True):
        i = order_dict[key] = menus_dict[key]
        i['class'] = 'hide'
        for child in i['children']:
            if child['id'] == getattr(request,settings.MENU):
                child['class'] = 'active'
                i['class'] = ''

    return {'menus_list': order_dict.values()}  # 使用字典返回到模板


# 从settings文件中获取session key的配置，与要展示按钮进行匹配，没有就不展示
@register.filter
def url_access(request, name):
    if name in request.session[settings.PERMISSION_SESSION_KEY]:
        return True


@register.inclusion_tag('breadcrumb.html')
def breadcrumb(request):
    breadcrumb_list = getattr(request,settings.BREADCRUMB)
    return {'breadcrumb_list':breadcrumb_list}
