from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('login', views.after_login, name='login1'),
    path('uploadedJob', views.uploadedJob, name='some_fun'),
    #re_path(r'^(?P<user_id>\d+)/$', views.deleteJob, name='urlname')
    path('<int:pk>/',
         views.specific_request, name='specific_request')
]
