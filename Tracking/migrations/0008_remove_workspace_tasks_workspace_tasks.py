# Generated by Django 5.0.3 on 2024-04-17 12:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tracking', '0007_remove_workspace_task_workspace_tasks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workspace',
            name='tasks',
        ),
        migrations.AddField(
            model_name='workspace',
            name='tasks',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='workspaces', to='Tracking.task'),
        ),
    ]
