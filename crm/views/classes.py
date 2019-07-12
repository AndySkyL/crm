from django.shortcuts import HttpResponse, reverse, render, redirect
from crm import models
from crm.forms import ClassForm


def class_list(request):
    all_class = models.Classlist.objects.all()
    return render(request, 'class_list.html', {'all_class': all_class})


def class_change(request, edit_id=None):
    obj = models.Classlist.objects.filter(pk=edit_id).first()
    form_obj = ClassForm(instance=obj)
    if request.method == 'POST':
        form_obj = ClassForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('class_list'))
    return render(request, 'class_edit.html', {'form_obj': form_obj})


def class_del(request, del_id):
    models.Classlist.objects.filter(pk=del_id).delete()
    return redirect(reverse('class_list'))
