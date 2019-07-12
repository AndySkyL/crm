from django.shortcuts import HttpResponse, render, redirect, reverse
from crm import models
from django.conf import settings
import hashlib


def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')

        # 对密码进行加密后校验
        md5 = hashlib.md5()
        md5.update(pwd.encode('utf-8'))
        obj = models.User.objects.filter(name=user, password=md5.hexdigest()).first()

        # 认证失败
        if not obj:
            return render(request, 'login.html', {"error": '用户名或密码不正确！'})

        # 认证成功,跨表查询对应的url权限和名称，同时过滤掉权限为空的数据记录
        permission_query = obj.roles.filter(permissions__url__isnull=False).values(
            'permissions__url',
            'permissions__title',
            'permissions__is_menu').distinct()

        permissions_list = []
        menu_list = []

        for i in permission_query:
            permissions_list.append({'url':i['permissions__url']})
            if i['permissions__is_menu']:
                menu_list.append({'title':i['permissions__title'],'url':i['permissions__url']})

        # print(permissions_list)
        # print(menu_list)
        # 将权限信息存入session 由于session中只支持json序列化的对象，所以转为list
        request.session[settings.PERMISSION_SESSION_KEY] = permissions_list
        request.session[settings.MENU_SESSION_KEY] = menu_list
        request.session['is_login'] = True

        return redirect(reverse('index'))

    return render(request, 'login.html')


def test(request):
    return render(request,'test.html',{'name':'andy'})