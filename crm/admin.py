from django.contrib import admin
from rbac import models
from crm.models import User


# 显示字段名称，和可编辑项
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'name','menu','parent']
    list_editable = ['url', 'name','menu','parent']


# 注册表
admin.site.register(models.Permission, PermissionAdmin)
admin.site.register(models.Role)
admin.site.register(User)
admin.site.register(models.Menu)
