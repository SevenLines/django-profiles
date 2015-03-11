from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.serializers import json, serialize
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from profiles.forms import ProfileForm, PasskeyForm
from profiles.models import Profile, ProfilePasskeys

session_passkeys = "passkeys"  # const, session variable which keeps all data


def check_passkey(fn):
    """
    checks if correct passkey present in session and redirects to provide passkey page otherwise
    :return:
    """

    def wrapper(request, id):
        if request.user.is_superuser:
            return fn(request, id)

        passkeys = request.session.get(session_passkeys)
        pkk = get_object_or_404(ProfilePasskeys, user_id=request.user.pk, profile_id=id)
        if passkeys and unicode(id) in passkeys and passkeys[unicode(id)] == pkk.passkey:
            return fn(request, id)
        else:
            if passkeys and unicode(id) in passkeys:
                messages.warning(request, 'wrong passkey')
            return redirect(reverse("profiles.views.profile.provide_passkey", args=[id, ]))

    return wrapper

def check_is_admin(fn):
    def wrapper(request, id):
        if request.user.is_superuser:
            return fn(request, id)

        if hasattr(request.user, 'is_admin') and request.user.is_admin:
            if request.user.is_superuser or request.user.profile.profiles.filter(pk=id).count():
                return fn(request, id)

        # if user dont have access for that profile
        return redirect(reverse("django.contrib.auth.views.login") + '?next=%s' % request.path)
    return wrapper
        # passkeys = request.session.get(session_passkeys)
        # pkk = get_object_or_404(ProfilePasskeys, user_id=request.user.pk, profile_id=id)
        # if passkeys and unicode(id) in passkeys and passkeys[unicode(id)] == pkk.passkey:
        #     return fn(request, id)
        # else:
        #     if passkeys and unicode(id) in passkeys:
        #         messages.warning(request, 'wrong passkey')
        #     return redirect(reverse("profiles.views.profile.provide_passkey", args=[id, ]))



@login_required
def provide_passkey(request, id):
    if request.method == "GET":
        form = PasskeyForm()
        return render(request, "profiles/manager/enter_passkey.html", {
            'form': form,
            'profile': get_object_or_404(Profile, pk=id)
        })
    elif request.method == "POST":
        form = PasskeyForm(request.POST)
        if form.is_valid():
            passkeys = request.session.get(session_passkeys, {})
            passkeys[id] = form.cleaned_data['passkey']
            request.session[session_passkeys] = passkeys
            return redirect(reverse("profiles.views.profile.update", args=[id]))
        else:
            return render(request, "profiles/manager/enter_passkey.html", {
                'form': form,
                'profile': get_object_or_404(Profile, pk=id)
            })

    return HttpResponseBadRequest()


def index(request):
    return render(request, "profiles/index.html", {
        'profiles': Profile.list_accessed_by(request.user),
        'allowed_profiles': request.user.profile.profiles.values_list("id", flat=True) if hasattr(request.user,
                                                                                                  'profile') else [],
    })


def show(request, id):
    profile = get_object_or_404(Profile, pk=id)

    def render_show_view(prf):
        return render(request, "profiles/show.html", {
            'profile': prf
        })

    passkeys = ProfilePasskeys.objects.filter(profile=profile)


    # anyone can see profile without passkey
    if passkeys.count() == 0:
        return render_show_view(profile)

    # if user is admin, check has he access for that profile
    if hasattr(request.user, 'is_admin') and request.user.is_admin:
        if request.user.is_superuser or request.user.profile.profiles.filter(pk=profile.id).count():
            return render_show_view(profile)

    # if user dont have access for that profile
    if passkeys.filter(user_id=request.user.pk).count() == 0:
        return redirect(reverse("django.contrib.auth.views.login") + '?next=%s' % request.path)

    pkk = get_object_or_404(ProfilePasskeys, user_id=request.user.pk, profile_id=id)
    passkeys = request.session.get(session_passkeys)
    if passkeys and unicode(id) in passkeys and passkeys[unicode(id)] == pkk.passkey:
        return render_show_view(profile)
    else:
        if passkeys and unicode(id) in passkeys:
            messages.warning(request, 'wrong passkey')
        return redirect(reverse("profiles.views.profile.provide_passkey", args=[id, ]))


def show_by_slug(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    return show(request, profile.pk)


@user_passes_test(lambda u: u.is_superuser)
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


@user_passes_test(lambda u: u.is_superuser)
def remove(request, id):
    profile = get_object_or_404(Profile, pk=id)
    profile.delete()
    if request.is_ajax():
        return HttpResponse()
    else:
        return redirect(reverse("profiles.views.profile.index"))


# @login_required
# @check_passkey
# @user_passes_test(lambda u: u.is_admin)
@check_is_admin
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

    # # if user is admin, check has he access for that profile
    # if hasattr(request.user, 'is_admin') and request.user.is_admin:
    #     if request.user.is_superuser or request.user.profile.profiles.filter(pk=profile.id).count():
    #         return render_show_view(profile)

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