from django.contrib import admin
from django.http.response import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path
from django.urls.base import reverse

from resources.forms.admin_forms import (
    ProtectedResourceAdminForm,
    ProtectedResourceUpdatePasswordAdminForm,
)
from resources.models import ProtectedResource
from resources.services import change_resource_password


@admin.register(ProtectedResource)
class ProtectedResourceAdmin(admin.ModelAdmin):
    change_form_template = "resources/admin/change_form.html"

    readonly_fields = (
        "created",
        "user",
        "id",
        "access_id",
        "password",
        "resource_type",
        "protected_url",
        "protected_file",
        "visits",
    )

    def get_changelist_form(self, request, **kwargs):
        return ProtectedResourceAdminForm

    def response_change(self, request, obj):
        if "_change_password" in request.POST:
            return HttpResponseRedirect(
                reverse("admin:resource_change_password", kwargs={"pk": obj.id})
            )
        return super().response_change(request, obj)

    def get_urls(self):
        urls = super().get_urls()

        extra_urls = [
            path(
                "change-password/<uuid:pk>/",
                self.change_password,
                name="resource_change_password",
            ),
        ]

        return extra_urls + urls

    def change_password(self, request, pk=None):
        if request.method != "POST":
            form = ProtectedResourceUpdatePasswordAdminForm()
        else:
            form = ProtectedResourceUpdatePasswordAdminForm(request.POST)
            if form.is_valid():
                obj = self.model.objects.get(pk=pk)
                change_resource_password(obj, form.cleaned_data["password"])

                self.message_user(request, "Password changed successfully.")
                return HttpResponseRedirect(
                    reverse("admin:resources_protectedresource_change", args=(obj.pk,))
                )

        context = self.admin_site.each_context(request)
        context["opts"] = self.model._meta
        context["form"] = form

        return TemplateResponse(
            request,
            "resources/admin/change_password.html",
            context=context,
        )
