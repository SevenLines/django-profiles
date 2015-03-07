from django.contrib.auth.decorators import login_required
from django.core.serializers import json, serialize
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from tastypie.http import HttpBadRequest
from profiles.forms import ProfileForm
from profiles.models import Profile


def index(request):
    return render(request, "profiles/index.html")


def show(request, id):
    profile = get_object_or_404(Profile, pk=id)
    return render(request, "profiles/show.html", {
        'profile': profile
    })


@login_required
def add(request):
    """
    add profile, on GET returns common profile-add-page
    on POST | validates sended data, on success: redirect to show page, on fail returns to add page
    on ajax POST | on success: returns updated profile, on fail returns errors
    :param request:
    :return:
    """
    context = {}
    if request.method == "GET":
        context['form'] = ProfileForm()
        return render(request, "profiles/add.html", context)
    elif request.method == "POST":
        form = ProfileForm(request.POST)
        context['form'] = ProfileForm()
        if form.is_valid():
            profile = form.save()
            if request.is_ajax():
                return HttpResponse(serialize('json', [profile, ]).strip("[]"))
            else:
                return redirect(reverse("profiles.views.show", args=[profile.pk]))
        else:
            if request.is_ajax():
                return HttpResponse(serialize('json', form.errors))
            else:
                return render(request, "profiles/add.html", context)
    return HttpBadRequest()


@login_required
def remove(request, id):
    profile = get_object_or_404(Profile, pk=id)
    profile.delete()
    return HttpResponse()


@login_required
def update(request, id):
    """
    updates profile by id, on GET returns common profile-update-page
    on POST | validates sended data, on success: redirect to show page, on fail returns to update page
    on ajax POST | on success: returns updated profile, on fail returns errors
    :param request:
    :param id:
    :return:
    """
    profile = get_object_or_404(Profile, pk=id)
    context = {
        'profile': profile
    }
    if request.method == "GET":
        context['form'] = ProfileForm(instance=profile)
        return render(request, "profiles/update.html", context)
    elif request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save()
            if request.is_ajax():
                return HttpResponse(serialize('json', [profile, ]).strip("[]"))
            else:
                return redirect(reverse("profiles.views.show", args=[profile.pk]))
        else:
            if request.is_ajax():
                return render(request, "profiles/update.html", context)
            else:
                return HttpResponse(serialize('json', form.errors))
    return HttpResponse()