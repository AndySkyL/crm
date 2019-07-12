from django.contrib import admin
from rbac import models
from crm.models import User


# 显示字段名称，和可编辑项
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'is_menu']
    list_editable = ['url', 'is_menu']


# 注册表
admin.site.register(models.Permission, PermissionAdmin)
admin.site.register(models.Role)
admin.site.register(User)
