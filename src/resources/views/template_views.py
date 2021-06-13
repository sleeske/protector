from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse, StreamingHttpResponse
from django.shortcuts import redirect, render
from django.views.generic.base import RedirectView, View
from django.views.generic.detail import (
    SingleObjectMixin,
    SingleObjectTemplateResponseMixin,
)
from django.views.generic.edit import FormView, ModelFormMixin, ProcessFormView

from resources.forms.template_forms import (
    ProtectedResourceAuthorizationForm,
    ProtectedResourceCreateForm,
)
from resources.models import ProtectedResource
from resources.services import (
    create_protected_resource_with_username_and_password,
    increment_visitors_count,
    is_resource_expired,
)
from resources.utils import chunked


def index(request, *args, **kwargs):
    return render(request, "resources/index.html")


class ProtectedResourceCreateView(LoginRequiredMixin, FormView):
    form_class = ProtectedResourceCreateForm
    template_name = "resources/create.html"
    success_template_name = "resources/created.html"

    def form_valid(self, form):
        obj = create_protected_resource_with_username_and_password(
            self.request.user, **form.cleaned_data
        )

        context = {
            "password": obj._password,
            "authorization_url": self.request.build_absolute_uri(
                obj.get_authorization_url()
            ),
        }

        return render(
            self.request,
            self.get_success_template(),
            context=context,
        )

    def get_success_template(self):
        return self.success_template_name


class ResourceAccessControlMixin:
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if is_resource_expired(self.object):
            return HttpResponse("Resource link expired.", status=410)

        return super().dispatch(request, *args, **kwargs)


class ProtectedResourceAuthorizationView(
    ResourceAccessControlMixin,
    SingleObjectTemplateResponseMixin,
    ModelFormMixin,
    ProcessFormView,
):
    form_class = ProtectedResourceAuthorizationForm
    template_name = "resources/authorize.html"
    model = ProtectedResource

    slug_field = "access_id"
    slug_url_kwarg = "access_id"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.object
        return kwargs

    def form_valid(self, form):
        increment_visitors_count(self.object)
        return redirect(self.object)


class ProtectedURLRedirectView(
    ResourceAccessControlMixin, SingleObjectMixin, RedirectView
):
    model = ProtectedResource

    def get_queryset(self):
        return super().get_queryset().urls_only()

    def get_redirect_url(self, *args, **kwargs):
        return self.object.protected_url


class ProtectedFileDownloadView(ResourceAccessControlMixin, SingleObjectMixin, View):
    model = ProtectedResource

    def get_queryset(self):
        return super().get_queryset().files_only()

    def get(self, request, *args, **kwargs):
        response = StreamingHttpResponse(chunked(self.object.protected_file))
        response["Content-Type"] = "application/octet-stream"
        response[
            "Content-Disposition"
        ] = f'attachment;filename="{self.object.protected_file.name}"'

        return response
