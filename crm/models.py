from django.db import models
from django.utils.safestring import mark_safe
from rbac.models import RbacUser


class Depart(models.Model):
    name = models.CharField(max_length=32, verbose_name='部门名称')
    desc = models.TextField(blank=True, null=True, verbose_name='描述')

    # 定义此属性，当从user表中查询部门的时候，可以自动展示对应的部门名称，而不是一个object对象
    def __str__(self):
        return self.name


# 继承rbac中的rbacuser表
class User(RbacUser,models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField('密码', max_length=32)
    gender = models.IntegerField('性别', choices=((0, '男'), (1, '女')))
    depart = models.ForeignKey('Depart', on_delete=models.CASCADE, verbose_name='部门')

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(verbose_name='课程名称', max_length=32)

    def __str__(self):
        return self.name


class School(models.Model):
    title = models.CharField(verbose_name='校区名称', max_length=32)

    def __str__(self):
        return self.title


class Classlist(models.Model):
    school = models.ForeignKey(verbose_name='校区', to='School')
    course = models.ForeignKey(verbose_name='课程名称', to='Course')
    semester = models.IntegerField(verbose_name='班级')
    price = models.IntegerField(verbose_name='学费')
    start_date = models.DateField(verbose_name='开班日期')
    graduate_date = models.DateField(verbose_name='结业日期', null=True, blank=True)
    tutor = models.ForeignKey(verbose_name='班主任', to='User', related_name='classes')
    teachers = models.ManyToManyField(verbose_name='任课老师', to='User', related_name='teach_classes')
    memo = models.CharField(verbose_name='说明', max_length=255, blank=True, null=True)

    def show_teachers(self):
        return ' | '.join([str(i.name) for i in self.teachers.all()])
