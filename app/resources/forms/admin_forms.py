from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from resources.models import ProtectedResource


class ProtectedResourceAdminForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = ProtectedResource
        fields = (
            "user",
            "id",
            "access_id",
            "password",
            "resource_type",
            "protected_url",
            "protected_file",
            "visits",
        )


class ProtectedResourceUpdatePasswordAdminForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data["password"] != cleaned_data["confirm_password"]:
            raise ValidationError(_("Provied passwords did not match"))

        return cleaned_data
