from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from profiles.models import Profile


def index(request):
    return render(request, "profiles/index.html")


def show(request, id):
    profile = get_object_or_404(Profile, pk=id)
    return render(request, "profiles/show.html", {
        'profile': profile
    })


@login_required
def add(request, id):
    profile = get_object_or_404(Profile, pk=id)
    if request.method == "GET":
        return render(request, "profiles/add.html", {
            'profile': profile
        })
    elif request.method == "POST":
        pass


@login_required
def remove(request, id):
    profile = get_object_or_404(Profile, pk=id)
    profile.delete()
    return HttpResponse()


@login_required
def update(request, id):
    profile = get_object_or_404(Profile, pk=id)
    if request.method == "GET":
        return render(request, "profiles/update.html", {
            'profile': profile
        })
    elif request.method == "POST":
        pass
    return HttpResponse()