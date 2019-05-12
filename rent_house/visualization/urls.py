from django.urls import path, re_path

from . import views


urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    path(r'index.html', views.index, name='index'),
    path(r'house_price.html', views.house_price, name='house_price'),
]

