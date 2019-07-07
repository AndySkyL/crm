from django.shortcuts import HttpResponse, reverse, render, redirect
from crm import models


def depart_list(request):
    all_depart = models.Depart.objects.all()

    # 获取url中的页面数，如果不是指定数字类型，就赋值为第一页
    try:
        page_num = int(request.GET.get('page', 1))
    except Exception as e:
        page_num = 1

    total_count = all_depart.count()  # 获取queryset对象中的数据数量
    per_num = 10  # 每页显示的数据条数
    page_disply = 11  # 显示的总分页数
    half_per = page_disply // 2
    page_total_num, more = divmod(total_count, per_num)  # 除法运算，返回两个数据，第一个为整除结果，第二个为余数

    # 如果有余数，页面数+1
    if more:
        page_total_num += 1
    start = (page_num - 1) * per_num
    end = page_num * per_num

    # 如果总页数小于要显示的页数，就显示全部分页号
    if page_total_num < page_disply:
        page_start = 1
        page_end = page_total_num

    # 如果总页数大于等于显示的固定页数，就自动向前后移动固定间隔的页码
    else:

        # 限制显示的负数页码
        if page_num <= half_per:
            page_start = 1
            page_end = page_disply

        # 限制超出页码
        elif page_num >= page_total_num - half_per:
            page_start = page_total_num - page_disply + 1
            page_end = page_total_num
        else:
            page_start = page_num - half_per
            page_end = page_num + half_per

    # 点击分页按钮的选中效果
    page_list = []

    # 添加向前翻页效果，在第一页时禁止向前翻页
    if page_num == 1:
        page_list.append(
            '<li class="disabled"><a aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>')
    else:
        page_list.append(
            '<li><a href="?page={}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'.format(
                page_num - 1))

    for i in range(page_start, page_end + 1):
        if i == page_num:  # 如果点击的分页正好是当前按钮，就添加选中效果
            page_list.append('<li class="active"><a href="?page={}">{}</a></li>'.format(i, i))
        else:
            page_list.append('<li><a href="?page={}">{}</a></li>'.format(i, i))

    # 添加向后翻页效果，在最后一页时，禁止向后翻页
    if page_num == page_total_num:
        page_list.append(
            '<li class="disabled"><a aria-label="Previous"><span aria-hidden="true">&raquo;</span></a></li>')
    else:
        page_list.append(
            '<li><a href="?page={}" aria-label="Previous"><span aria-hidden="true">&raquo;</span></a></li>'.format(
                page_num + 1))

    # 生成html页面
    page_html = ''.join(page_list)

    return render(request, 'depart_list.html',
                  {'all_depart': all_depart[start:end], 'page_html': page_html})


from django import forms


# 使用ModelForm进行处理
class DepartForm(forms.ModelForm):
    # name = forms.CharField(validators=[],) # 可以增加字段，也可以对字段进行重写
    class Meta:
        model = models.Depart
        fields = "__all__"  # ['name','desc']   可以指定字段,使用all表示所有字段，定义是有序的
        # exclude = ['desc']  # 这里也可以使用exclude排除指定的字段

        # 可以给单个模板对象添加样式
        widgets = {
            # 'name': forms.TextInput(attrs={'class':'form-control'})
        }

        # 可以使用如下方式修改部门名称
        # labels= {
        #     'name':'部门名称'
        # }

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
