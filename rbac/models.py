from django.db import models


# 权限表
class Permission(models.Model):
    url = models.CharField('含正则的URL', max_length=128)
    title = models.CharField('标题', max_length=32, blank=True, null=True)
    is_menu = models.BooleanField('是否是菜单', default=False)

    def __str__(self):
        return self.title


# 角色表
class Role(models.Model):
    name = models.CharField('角色名称', max_length=32)
    permissions = models.ManyToManyField('Permission', verbose_name='角色拥有的权限', blank=True)

    def __str__(self):
        return self.name


# 用户表
class RbacUser(models.Model):
    # name = models.CharField('用户名',max_length=32)
    # password = models.CharField('密码',max_length=32)
    roles = models.ManyToManyField(Role, verbose_name='用户拥有的角色', blank=True)  # Role使用类生成对应关系

    class Meta:
        abstract = True  # 数据库迁移时不生成表，这张表当做基类用作继承。
