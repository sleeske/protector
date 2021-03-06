# Generated by Django 3.1.12 on 2021-06-13 22:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import resources.utils
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProtectedResource',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('access_id', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('password', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('resource_type', models.PositiveSmallIntegerField(choices=[(0, 'url'), (1, 'file')])),
                ('protected_url', models.URLField(blank=True, verbose_name='URL')),
                ('protected_file', models.FileField(blank=True, upload_to=resources.utils.files.create_uuid_filename, verbose_name='file')),
                ('visits', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'protected resource',
                'verbose_name_plural': 'protected resources',
            },
        ),
    ]
