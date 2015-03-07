from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.serializers import json, serialize
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect

from profiles.forms import ProfileForm, PasskeyForm, ProfilePasskeysForm
from profiles.models import Profile, ProfilePasskeys


@login_required
def manager(request):
    context = {
        'users': User.objects.all(),
        'profiles': Profile.objects.all(),
    }
    return render(request, "profiles/manager/manager.html", context)


@login_required
def get_profile_users(request, profile_id):
    """
    :return: list of users which can work with profile with profile_id
    """
    data = User.objects.filter(pk__in=ProfilePasskeys.objects.filter(profile=profile_id).values("user"))
    data = serialize('json', data)
    return HttpResponse(data, content_type='json')


@login_required
def get_user_profiles(request, user_id):
    """
    :return: list of profiles with which user can work
    """
    user = get_object_or_404(User, pk=user_id)
    data = serialize('json', ProfilePasskeys.objects.filter(user=user))
    return HttpResponse(data, content_type='json')


@login_required
def add_user_to_profile(request, user_id, profile_id):
    """
    add to user ability to work with profile
    """
    profile = get_object_or_404(Profile, pk=profile_id)
    if request.method == "GET":
        form = PasskeyForm()
        return render(request, "profiles/manager/add_user_to_profile.html", {
            'form': form
        })
    elif request.method == "POST":
        form = PasskeyForm(request.POST)
        if form.is_valid():
            ppk = ProfilePasskeys.objects.get_or_create(profile_id=profile_id, user_id=user_id)
            ppk.passkey = form.cleande_data['passkey']
            ppk.save()
            return HttpResponse()
        elif request.is_ajax():
            return HttpResponseBadRequest()
        else:
            return render(request, "profiles/manager/add_user_to_profile.html", {
                'form': form
            })
    return HttpResponseBadRequest()


@login_required
def remove_user_from_profile(request, user_id, profile_id):
    passkey_obj = get_object_or_404(ProfilePasskeys, profile_id=profile_id, user_id=user_id)
    passkey_obj.delete()
    return HttpResponse()


@login_required
def update_user_profile_passkey(request, user_id, profile_id):
    passkey_obj = get_object_or_404(ProfilePasskeys, profile_id=profile_id, user_id=user_id)
    if request.method == "GET":
        form = ProfilePasskeysForm()
        return render(request, "profiles/manager/update_user_profile_passkey.html", {
            'form': form
        })
    elif request.method == "POST":
        form = ProfilePasskeysForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse()
        elif request.is_ajax():
            return HttpResponseBadRequest()
        else:
            return render(request, "profiles/manager/update_user_profile_passkey.html", {
                'form': form
            })
    return HttpResponseBadRequest()


@login_required
def check_passkey(request, profile_id):
    """
    Checks is user can access profile with profile_id
    on GET show input password form
    on POST  try to enter: on success returns edit page, on fail redirects back
    """
    profile = get_object_or_404(Profile, pk=profile_id)
    if request.method == "GET":
        form = PasskeyForm()
        return render(request, "profiles/manager/check_passkey.html", {
            'form': form
        })
    elif request.method == "POST":
        form = PasskeyForm(request.POST)
        if form.is_valid():
            passkey = form.cleaned_data['passkey']
            if profile.can_be_accessed(passkey, request.user):
                return redirect(reverse("profiles.views.profile.show", args=[profile_id]))
            else:
                form.add_error(None, "wrong passkey")
        return render(request, "profiles/manager/check_passkey.html", {
            'form': form
        })
    return HttpResponseBadRequest()