import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.core.urlresolvers import reverse
from django.db.transaction import atomic
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from app.utils import require_in_POST

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
@require_POST
@require_in_POST('profile_passkeys')
@atomic
def update_profile_passkeys(request):
    """
    this view expects POST method,
    expects the list of triples in profile_passkeys parameter

      {profile: 'profile_id', user: 'user_id', passkey: 'some_passkey'}

    to mark triple as to remove add allowed parameter

      {profile: 'profile_id', user: 'user_id', passkey: 'some_passkey', allowed: 'false'}

    """
    profiles_passkeys = json.loads(request.POST['profile_passkeys'])
    for profile_passkey in profiles_passkeys:
        profile_id = profile_passkey['profile']
        user_id = profile_passkey['user']

        if 'allowed' in profile_passkey:
            if profile_passkey['allowed'] == False:
                ppk = ProfilePasskeys.objects.filter(profile_id=profile_id, user_id=user_id)
                ppk.delete()
                continue

        passkey = profile_passkey['passkey']
        if passkey == '':
            continue
        ppk, _ = ProfilePasskeys.objects.get_or_create(profile_id=profile_id, user_id=user_id)
        ppk.passkey = passkey
        ppk.save()
    return HttpResponse()


#
# @login_required
# def get_profile_users(request, profile_id):
# """
#     :return: list of users which can work with profile with profile_id
#     """
#     data = User.objects.filter(pk__in=ProfilePasskeys.objects.filter(profile=profile_id).values("user"))
#     data = serialize('json', data)
#     return HttpResponse(data, content_type='json')
#
#
# @login_required
# def get_user_profiles(request, user_id):
#     """
#     :return: list of profiles with which user can work
#     """
#     user = get_object_or_404(User, pk=user_id)
#     data = serialize('json', ProfilePasskeys.objects.filter(user=user))
#     return HttpResponse(data, content_type='json')
#
#
# @login_required
# def add_user_to_profile(request, user_id, profile_id):
#     """
#     add to user ability to work with profile
#     """
#     profile = get_object_or_404(Profile, pk=profile_id)
#     if request.method == "GET":
#         form = PasskeyForm()
#         return render(request, "profiles/manager/add_user_to_profile.html", {
#             'form': form
#         })
#     elif request.method == "POST":
#         form = PasskeyForm(request.POST)
#         if form.is_valid():
#             ppk = ProfilePasskeys.objects.get_or_create(profile_id=profile_id, user_id=user_id)
#             ppk.passkey = form.cleande_data['passkey']
#             ppk.save()
#             return HttpResponse()
#         elif request.is_ajax():
#             return HttpResponseBadRequest()
#         else:
#             return render(request, "profiles/manager/add_user_to_profile.html", {
#                 'form': form
#             })
#     return HttpResponseBadRequest()
#
#
# @login_required
# def remove_user_from_profile(request, user_id, profile_id):
#     passkey_obj = get_object_or_404(ProfilePasskeys, profile_id=profile_id, user_id=user_id)
#     passkey_obj.delete()
#     return HttpResponse()
#
#
# @login_required
# def update_user_profile_passkey(request, user_id, profile_id):
#     passkey_obj = get_object_or_404(ProfilePasskeys, profile_id=profile_id, user_id=user_id)
#     if request.method == "GET":
#         form = ProfilePasskeysForm()
#         return render(request, "profiles/manager/update_user_profile_passkey.html", {
#             'form': form
#         })
#     elif request.method == "POST":
#         form = ProfilePasskeysForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponse()
#         elif request.is_ajax():
#             return HttpResponseBadRequest()
#         else:
#             return render(request, "profiles/manager/update_user_profile_passkey.html", {
#                 'form': form
#             })
#     return HttpResponseBadRequest()


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