from django import forms
from profiles.models import Profile, ProfilePasskeys


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'text']


class ProfilePasskeysForm(forms.ModelForm):
    class Meta:
        model = ProfilePasskeys
        fields = ['user', 'passkey', 'profile']


class PasskeyForm(forms.Form):
    passkey = forms.CharField(max_length=128, required=True)