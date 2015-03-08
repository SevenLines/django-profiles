import json
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.serializers import serialize
from django.core.urlresolvers import reverse
from django.db.transaction import atomic
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.decorators.http import require_POST
from app.utils import require_in_POST, require_in_GET

from profiles.forms import ProfileForm, PasskeyForm, ProfilePasskeysForm
from profiles.models import Profile, ProfilePasskeys


@user_passes_test(lambda u: u.is_superuser)
def manager(request):
    context = {
        'users': User.objects.all(),
        'profiles': Profile.objects.all(),
    }
    return render(request, "profiles/manager/manager.html", context)


@user_passes_test(lambda u: u.is_superuser)
@require_in_POST("user_id", "profile_id")
def send_passkey_to_email(request,):
    """
    sends message to user with info about new password
    :return:
    """
    user = get_object_or_404(User, pk=request.POST['user_id'])
    profile = get_object_or_404(Profile, pk=request.POST['profile_id'])

    passkey = get_object_or_404(ProfilePasskeys, user=user, profile=profile)

    message_html = render_to_string("profiles/emails/passkey_update.html", {
        "user": user,
        "profile": profile,
        "passkey": passkey,
        "profile_update_url": request.build_absolute_uri(reverse('profiles.views.profile.update', args=[profile.pk]))
    })

    user.email_user("New passkey", strip_tags(message_html), settings.EMAIL_USERNAME, fail_silently=False, html_message=message_html)

    return HttpResponse()


@user_passes_test(lambda u: u.is_superuser)
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