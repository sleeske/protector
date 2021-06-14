from django import forms
from django.utils.translation import gettext as _


class ProtectedResourceCreateForm(forms.Form):
    protected_url = forms.CharField(required=False)
    protected_file = forms.FileField(required=False)


class ProtectedResourceAuthorizationForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
