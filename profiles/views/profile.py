from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.serializers import json, serialize
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from profiles.forms import ProfileForm
from profiles.models import Profile, ProfilePasskeys


def index(request):
    return render(request, "profiles/index.html", {
        'profiles': Profile.objects.all()
    })


def show(request, id):
    profile = get_object_or_404(Profile, pk=id)
    return render(request, "profiles/show.html", {
        'profile': profile
    })


def show_by_slug(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
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
                if profile.slug:
                    return redirect(reverse("profiles.views.profile.show_by_slug", args=[profile.slug]))
                else:
                    return redirect(reverse("profiles.views.profile.show", args=[profile.pk]))
        else:
            if request.is_ajax():
                return HttpResponse(serialize('json', form.errors))
            else:
                return render(request, "profiles/add.html", context)
    return HttpResponseBadRequest()


@login_required
def remove(request, id):
    profile = get_object_or_404(Profile, pk=id)
    profile.delete()
    if request.is_ajax():
        return HttpResponse()
    else:
        return redirect(reverse("profiles.views.profile.index"))


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
                if profile.slug:
                    return redirect(reverse("profiles.views.profile.show_by_slug", args=[profile.slug]))
                else:
                    return redirect(reverse("profiles.views.profile.show", args=[profile.pk]))
        else:
            if request.is_ajax():
                return render(request, "profiles/update.html", context)
            else:
                return HttpResponse(serialize('json', form.errors))
    return HttpResponse()