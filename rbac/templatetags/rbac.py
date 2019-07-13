from django.template import Library
from django.conf import settings
import re

register = Library()


@register.inclusion_tag('menu.html')
def menu(request):
    menus_list = request.session[settings.MENU_SESSION_KEY]
    for i in menus_list:
        if re.match('^{}$'.format(i['url']), request.path_info):
            i['class'] = 'active'
    return {'menus_list': menus_list}  # 使用字段返回到模板


# 从settings文件中获取session key的配置，与要展示按钮进行匹配，没有就不展示
@register.filter
def url_access(request, name):
    if name in request.session[settings.PERMISSION_SESSION_KEY]:
        return True
