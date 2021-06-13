from django import forms
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from resources.models import ProtectedResource


class ProtectedResourceCreateForm(forms.Form):
    protected_url = forms.CharField(required=False)
    protected_file = forms.FileField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        protected_url = cleaned_data.get("protected_url")
        protected_file = cleaned_data.get("protected_file")

        if not protected_url and not protected_file:
            raise ValidationError("Provice an URL or a file to protect.")

        if protected_url and protected_file:
            raise ValidationError(
                "Provice either an URL or a file to protect, not both."
            )


class ProtectedResourceAuthorizationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = ProtectedResource
        fields = ("password",)
        widgets = {"password": forms.PasswordInput()}

    def clean_password(self):
        password = self.cleaned_data["password"]

        if not check_password(password, self.instance.password):
            raise ValidationError("Invalid password")

        return password
