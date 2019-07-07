from django.shortcuts import HttpResponse, reverse, render, redirect
from crm import models
from django import forms


def user_list(request):
    all_user = models.User.objects.all()
    return render(request, 'user_list.html', {'all_user': all_user})


class UserForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = '__all__'
        labels= {
            'name':'用户名'
        }

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'password':forms.PasswordInput(attrs={'class':'form-control'}),
            'gender':forms.Select(attrs={'class':'form-control'}),
            'depart':forms.Select(attrs={'class':'form-control'})
        }

def user_add(request):
    form_obj = UserForm()
    if request.method == 'POST':
        form_obj = UserForm(request.POST)
        if form_obj.is_valid():
            # 保存到数据库中
            # models.Depart.objects.create(**form_obj.cleaned_data)
            form_obj.save()
            return redirect(reverse('user_list'))
    return render(request, 'user_add.html', {'form_obj': form_obj})


def user_edit(request,edit_id):
    obj = models.User.objects.filter(pk=edit_id).first()
    form_obj = UserForm(instance=obj)
    if request.method == 'POST':
        form_obj = UserForm(request.POST,instance=obj)
        if form_obj.is_valid():
            # 保存到数据库中
            # models.Depart.objects.create(**form_obj.cleaned_data)
            form_obj.save()
            return redirect(reverse('user_list'))
    return render(request, 'user_edit.html', {'form_obj': form_obj})


def user_del(request,del_id):
    models.User.objects.filter(pk=del_id).delete()
    return redirect(reverse('user_list'))