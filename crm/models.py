from django.db import models


class Depart(models.Model):
    name = models.CharField(max_length=32, verbose_name='部门名称')
    desc = models.TextField(blank=True, null=True, verbose_name='描述')

# 定义此属性，当从user表中查询部门的时候，可以自动展示对应的部门名称，而不是一个object对象
    def __str__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField('密码',max_length=32)
    gender = models.IntegerField('性别',choices=((0, '男'), (1, '女')))
    depart = models.ForeignKey('Depart', on_delete=models.CASCADE,verbose_name='部门')

