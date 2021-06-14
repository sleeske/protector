import uuid

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from resources.constants import RESOURCE_TYPES, TYPE_FILE, TYPE_URL
from resources.managers import ProtectedResourceQuerySet
from resources.utils.files import create_uuid_filename


class ProtectedResource(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    access_id = models.UUIDField(unique=True, default=uuid.uuid4)

    password = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    resource_type = models.PositiveSmallIntegerField(choices=RESOURCE_TYPES)
    protected_url = models.URLField(_("URL"), blank=True)
    protected_file = models.FileField(
        _("file"), blank=True, upload_to=create_uuid_filename
    )
    visits = models.IntegerField(default=0)

    # Auto-generatated password, returned just once to user
    _password = None

    objects = ProtectedResourceQuerySet.as_manager()

    class Meta:
        verbose_name = _("protected resource")
        verbose_name_plural = _("protected resources")

    def clean(self):
        if not self.protected_url and not self.protected_file:
            raise ValidationError("Provice an URL or a file to protect.")

        if self.protected_url and self.protected_file:
            raise ValidationError(
                "Provice either an URL or a file to protect, not both."
            )

    def save(self, *args, **kwargs):
        self.resource_type = TYPE_URL if self.protected_url else TYPE_FILE
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        if self.resource_type == TYPE_URL:
            view_name = "resources:redirect"
        else:
            view_name = "resources:download"

        return reverse(view_name, kwargs={"pk": self.id})

    def get_authorization_url(self):
        return reverse("resources:authorize", kwargs={"access_id": self.access_id})

    def get_api_authorization_url(self):
        return reverse("resources:api-authorize", kwargs={"access_id": self.access_id})
