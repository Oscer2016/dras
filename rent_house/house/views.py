from django.http import HttpResponse
from django.shortcuts import render
from house.models import User


def index(request):
    #return HttpResponse("Hello, you're at the house index.")
    return render(request, "house/index.html")


def register(request):
    return render(request, "house/reg.html")


def login(request):
    return render(request, "house/login.html")


def user(request):
    return render(request, "house/user.html")


def house(request):
    return render(request, "house/pro.html")


def detail(request):
    return render(request, "house/proinfo.html")


def ranking(request):
    return render(request, "house/pro_ranking.html")


def new(request):
    return render(request, "house/pro_new.html")


def reg_user(request):
    
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = User(username=username, password=password)
        user.save()

    return render(request, "house/login.html")


def login_user(request):

    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get('password')

        print(username)
        print(password)

    return render(request, "house/index.html")

