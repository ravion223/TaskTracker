# Generated by Django 5.0.3 on 2024-04-17 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tracking', '0008_remove_workspace_tasks_workspace_tasks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workspace',
            name='tasks',
        ),
        migrations.AddField(
            model_name='workspace',
            name='tasks',
            field=models.ManyToManyField(blank=True, related_name='workspaces', to='Tracking.task'),
        ),
    ]
