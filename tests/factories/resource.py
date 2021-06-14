import factory
from resources.constants import TYPE_URL
from resources.models import ProtectedResource

from .user import UserFactory


class ProtectedResourceFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    class Meta:
        abstract = True
        model = ProtectedResource


class ProtectedURLResourceFactory(ProtectedResourceFactory):
    protected_url = factory.Faker("url")
    resource_type = TYPE_URL
