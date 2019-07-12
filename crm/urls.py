from django.conf.urls import url,include
from crm.views import home
from crm.views import depart,user,classes


urlpatterns = [

    url(r'^login/', home.login,name='login'),
    url(r'^index/', home.index,name='index'),
    url(r'^depart/list/',depart.depart_list,name='depart_list'),
    url(r'^depart/add/', depart.depart_add,name='depart_add'),
    url(r'^depart/edit/(\d+)/', depart.depart_edit, name='depart_edit'),
    url(r'^depart/del/(\d+)/', depart.depart_del, name='depart_del'),

    url(r'^user/list/',user.user_list,name='user_list'),
    url(r'^user/add/', user.user_add, name='user_add'),
    url(r'^user/edit/(\d+)/', user.user_edit, name='user_edit'),
    url(r'^user/del/(\d+)/', user.user_del, name='user_del'),

    url(r'^class/list/',classes.class_list,name='class_list'),
    url(r'^class/add/', classes.class_change, name='class_add'),
    url(r'^class/edit/(\d+)/', classes.class_change, name='class_edit'),
    url(r'^class/del/(\d+)/', classes.class_del, name='class_del'),

]
