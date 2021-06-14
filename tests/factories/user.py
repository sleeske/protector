import factory
from django.contrib.auth import get_user_model


class UserFactory(factory.django.DjangoModelFactory):
    username = "Admin"
    email = "admin@testcase.com"
    is_superuser = False
    is_staff = False

    class Meta:
        model = get_user_model()
