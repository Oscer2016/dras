from django.urls import path, re_path

from . import views


urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    path(r'index.html', views.index, name='index'),
    path(r'reg.html', views.register, name='register'),
    path(r'login.html', views.login, name='login'),
    path(r'user.html', views.user, name='user'),
    path(r'pro.html', views.house, name='house'),
    path(r'proinfo.html', views.detail, name='detail'),
    path(r'pro_ranking.html', views.ranking, name='ranking'),
    path(r'pro_new.html', views.new, name='new'),
    path(r'reg_user/', views.reg_user, name='reg_user'),
    path(r'login_user/', views.login_user, name='login_user'),
]

