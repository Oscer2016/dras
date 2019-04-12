#from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    #return HttpResponse("Hello, you're at the house index.")
    return render(request, "house/index.html")


def register(request):
    return render(request, "house/reg.html")


def login(request):
    return render(request, "house/login.html")


def user(request):
    return render(request, "house/user.html")

