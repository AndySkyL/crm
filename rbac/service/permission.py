from django.conf import settings


def init_permission(request, obj):
    # 认证成功,跨表查询对应的url权限和名称，同时过滤掉权限为空的数据记录
    permission_query = obj.roles.filter(permissions__url__isnull=False).values(
        'permissions__url',
        'permissions__title',
        'permissions__name',
        'permissions__is_menu').distinct()

    permissions_dict = {}  # 定义为字典类型
    menu_list = []

    '''
    permissions_dict定义为{'depart_add':{'url':'/crm/depart/add/'},
                          'user_add':{'url':'/crm/user/add/'}} 的形式
    '''

    for i in permission_query:
        permissions_dict[i['permissions__name']] = {'url': i['permissions__url']}
        if i['permissions__is_menu']:
            menu_list.append({'title': i['permissions__title'], 'url': i['permissions__url']})

    # 将权限信息存入session 由于session中只支持json序列化的对象，所以转为list
    request.session[settings.PERMISSION_SESSION_KEY] = permissions_dict
    request.session[settings.MENU_SESSION_KEY] = menu_list
    request.session['is_login'] = True
