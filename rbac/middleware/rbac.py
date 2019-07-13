from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
from django.conf import settings
import re


class RbacMiddleWare(MiddlewareMixin):
    def process_request(self, request):

        # 获取当前的url地址
        url = request.path_info

        # 白名单的校验,使用正则匹配url
        for i in settings.VALID_URL:
            if re.match(i, url):
                return

        # 白名单的校验，验证登录用户
        try:
            is_login = request.session['is_login']
        except Exception:
            is_login = False
        if not is_login:
            return HttpResponse('未登录')
        for i in settings.LOGIN_URL:
            if re.match(i, url):
                return

        # 获取登录用的session,得到权限信息
        permission_dict = request.session[settings.PERMISSION_SESSION_KEY]

        # 访问的url与session中的权限进行正则匹配
        for i in permission_dict.values():
            if re.match('^{}$'.format(i['url']), url):
                return
        return HttpResponse('无权限访问！')
