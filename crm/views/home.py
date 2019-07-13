from django.shortcuts import HttpResponse, render, redirect, reverse
from crm import models
from rbac.service.permission import init_permission
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

        # 认证成功 进行权限信息初始化
        init_permission(request,obj)

        return redirect(reverse('index'))

    return render(request, 'login.html')


