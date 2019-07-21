from django.conf import settings


def init_permission(request, obj):
    # 认证成功,跨表查询对应的url权限和名称，同时过滤掉权限为空的数据记录
    permission_query = obj.roles.filter(permissions__url__isnull=False).values(
        'permissions__url',
        'permissions__title',
        'permissions__name',
        'permissions__menu',
        'permissions__menu__title',
        'permissions__menu__icon',
        'permissions__menu__weight',
        'permissions__id',
        'permissions__parent',
        'permissions__parent__name').distinct()

    permissions_dict = {}  # 定义为字典类型

    menu_dict = {}

    '''
    permissions_dict定义为{'depart_add':{'url':'/crm/depart/add/'},
                          'user_add':{'url':'/crm/user/add/'}} 的形式
                          
    menu_dict 定义为：{
        一级菜单ID:{
                    title: 信息管理,
                    icon: fa-ravelry,
                    children: [{'permissions__title': '班级列表','permissions__url': '/crm/class/list/'},
                               {'permissions__title': '部门列表','permissions__url': '/crm/depart/list/'}
                              ]   
	            } 
	                 } 的形式
    '''

    for n in permission_query:
        permissions_dict[n['permissions__name']] = {'url': n['permissions__url'],
                                                    'id':n['permissions__id'],
                                                    'pid':n['permissions__parent'],
                                                    'title':n['permissions__title'],
                                                    'pname':n['permissions__parent__name']
                                                    }
        if not n['permissions__menu']:
            continue
        if n['permissions__menu'] in menu_dict:
            menu_dict[n['permissions__menu']]['children'].append({'title': n['permissions__title'],
                                                                  'url': n['permissions__url'],
                                                                  'id': n['permissions__id']})
        else:
            menu_dict[n['permissions__menu']] = {'title': n['permissions__menu__title'],
                                                 'icon': n['permissions__menu__icon'],
                                                 'weight': n['permissions__menu__weight'],
                                                 'children': [{'title': n['permissions__title'],
                                                               'url': n['permissions__url'],
                                                               'id':n['permissions__id']}]}
    # 将权限信息存入session 由于session中只支持json序列化的对象，所以转为list
    request.session[settings.PERMISSION_SESSION_KEY] = permissions_dict
    request.session[settings.MENU_SESSION_KEY] = menu_dict
    request.session['is_login'] = True
