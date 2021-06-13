from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserAgentTracker(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="user_agent_tracker",
    )
    user_agent = models.TextField()

    class Meta:
        verbose_name = _("user agent tracker")
