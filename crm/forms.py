from django import forms
from crm import models
from django.core.exceptions import ValidationError
import hashlib

# 使用ModelForm进行处理
class DepartForm(forms.ModelForm):
    class Meta:
        model = models.Depart
        fields = "__all__"  # ['name','desc']   可以指定字段,使用all表示所有字段，定义是有序的

        error_messages = {
            'name': {
                'required': '不能为空'
            }
        }

    # 给所有模板对象批量添加样式
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():  # field字段的对象
            field.widget.attrs.update({'class': 'form-control'})  # 拿到对象的属性，添加属性


class UserForm(forms.ModelForm):

    # 对密码框校验规则进行重写
    password = forms.CharField(
        label='密码',
        min_length=6,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    # 增加确认密码输入框
    re_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control'},))

    class Meta:
        model = models.User
        # fields = '__all__'

        # fields中可以自定义显示的顺序
        fields = ['name','password','re_password','gender','depart']
        labels = {
            'name': '用户名',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'depart': forms.Select(attrs={'class': 'form-control'})
        }

    # 使用去全局钩子验证密码
    def clean(self):
        pwd = self.cleaned_data.get('password')
        re_pwd=self.cleaned_data.get('re_password')
        # 通过校验
        if pwd == re_pwd and pwd is not None:

            print(pwd,re_pwd)
            #对数据进行加密
            md5 = hashlib.md5()
            md5.update(pwd.encode('utf-8'))
            self.cleaned_data['password'] = md5.hexdigest()
            return self.cleaned_data

        # 没有通过校验
        self.add_error('re_password','两次密码不一致！')

        # 错误提示会加到__all__中。在模板使用form_obj.non_field_errors可以显示该错误
        raise ValidationError('两次密码不一致')



class ClassForm(forms.ModelForm):
    class Meta:
        model = models.Classlist
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
