from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "profiles/index.html")


def show(request, id):
    return render(request, "")


@login_required
def add(request, id):
    return HttpResponse()


@login_required
def remove(request, id):
    return HttpResponse()


@login_required
def update(request, id):
    return HttpResponse()