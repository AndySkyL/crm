from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
from django.conf import settings
import re


class RbacMiddleWare(MiddlewareMixin):
    def process_request(self, request):


        setattr(request,settings.MENU,None)
        # request.breadcrumb_list = [{'url': '/crm/index', 'title': '首页'}]  # 普通方式
        setattr(request,settings.BREADCRUMB,[{'url': '/crm/index', 'title': '首页'}])  # 使用反射可以更加灵活的设置
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
                pid = i.get('pid')
                id = i.get('id')
                pname = i.get('pname')
                breadcrumb_list = getattr(request,settings.BREADCRUMB)
                if pid:
                    # 当前访问的是二级菜单下的子权限记录此二级菜单的值
                    # request.current_id = pid
                    setattr(request,settings.MENU,pid)
                    breadcrumb_list.append(
                        {'url': permission_dict[pname]['url'], 'title': permission_dict[pname]['title']})

                else:
                    # 当前访问的是二级菜单，就记录此二级菜单的值
                    # request.current_id = id
                    setattr(request,settings.MENU,id)
                breadcrumb_list.append({'url': i['url'], 'title': i['title']})

                return
        return HttpResponse('无权限访问！')
