from django.db import models



class Menu(models.Model):
    '''
    一级菜单
    '''
    title = models.CharField(max_length=32)
    icon = models.CharField(max_length=32)   # 存放图标的样式
    weight = models.IntegerField(default=1) # 设置默认权重为1

    def __str__(self):
        return self.title



# 权限表
class Permission(models.Model):
    url = models.CharField('含正则的URL', max_length=128)
    title = models.CharField('标题', max_length=32, blank=True, null=True)
    name = models.CharField('URL别名',max_length=32,unique=True)
    menu = models.ForeignKey('Menu',blank=True,null=True)   # 关联一级菜单的ID
    parent = models.ForeignKey('Permission',blank=True,null=True)   # 关联自身表中二级菜单的ID

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
