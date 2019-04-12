from django.urls import path, re_path

from . import views


urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    path(r'index.html', views.index, name='index'),
    path(r'reg.html', views.register, name='register'),
    path(r'login.html', views.login, name='login'),
    path(r'user.html', views.user, name='user')
]

