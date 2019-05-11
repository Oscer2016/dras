from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect


def index(request):
    #return HttpResponse("Hello, you're at the visualization index.")
    return render(request, "visualization/index.html")

