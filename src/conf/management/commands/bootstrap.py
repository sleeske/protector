from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Bootstraps the environment"

    def handle(self, *args, **options):
        call_command("migrate", interactive=False)

        if not settings.DEBUG:
            return

        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            # Just to make life easier
            username = "admin"
            email = "test@mail.com"
            password = "test123"

            User.objects.create_superuser(
                username=username, email=email, password=password
            )
            print(f"Created Superuser with username {username}, password: {password}")
