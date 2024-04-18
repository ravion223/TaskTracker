# Generated by Django 5.0.3 on 2024-04-18 07:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tracking', '0010_task_workspace'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='workspace',
            name='allowed_users',
            field=models.ManyToManyField(blank=True, related_name='allowed_workspace', to=settings.AUTH_USER_MODEL),
        ),
    ]