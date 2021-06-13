from django.utils.translation import gettext_lazy as _

TYPE_URL = 0
TYPE_FILE = 1

RESOURCE_TYPES = (
    (TYPE_URL, _("url")),
    (TYPE_FILE, _("file")),
)
