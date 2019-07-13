from django.shortcuts import HttpResponse, reverse, render, redirect
from crm import models
from utils.pagination import Pagination
from crm.forms import DepartForm
from django.http.request import QueryDict

def depart_list(request):
    all_depart = models.Depart.objects.all()

    print(request.GET.copy().urlencode())
    pages = Pagination(all_depart.count(), request.GET.get('page', 1))

    return render(request, 'depart_list.html',
                  {'all_depart': all_depart[pages.start:pages.end], 'page_html': pages.page_html})




def depart_add(request):
    form_obj = DepartForm()
    if request.method == 'POST':
        form_obj = DepartForm(request.POST)
        if form_obj.is_valid():
            # 保存到数据库中
            # models.Depart.objects.create(**form_obj.cleaned_data)
            form_obj.save()
            return redirect(reverse('depart_list'))
    return render(request, 'depart_add.html', {'form_obj': form_obj})


def depart_edit(request, edit_id):
    obj = models.Depart.objects.filter(pk=edit_id).first()
    print(obj)
    form_obj = DepartForm(instance=obj)  # 传入实例对象
    if request.method == 'POST':
        form_obj = DepartForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('depart_list'))

    return render(request, 'depart_edit.html', {'form_obj': form_obj})


# def depart_del(request, del_id):
#     models.Depart.objects.filter(pk=del_id).delete()
#     return redirect(reverse('depart_list'))

from django.http import JsonResponse


def depart_del(request, del_id):
    ret = {'status': 0, 'msg': None}  # 定义一个字典，如果成功就返回默认值
    try:  # 尝试删除，删除失败抛出异常
        models.Depart.objects.filter(pk=del_id).delete()

    except Exception as e:
        ret['status'] = 1
        ret['msg'] = str(e)

    return JsonResponse(ret)  # 使用Jsonresponse格式返回ret结果
