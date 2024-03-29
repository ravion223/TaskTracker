from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):

    STATUS_CHOICES = [
        ('todo', "To Do"),
        ('in_progress', "In progress"),
        ('done', 'Done')
    ]

    PRIORITY_CHOICES = [
        ('low', "Low"),
        ('medium', "Medium"),
        ('high', 'High'),
        ('critical', 'Critical')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    title = models.CharField(max_length=63)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='low')
    due_date = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.title} - {self.status} - {self.priority}"
    
    class Meta:
        ordering = ["due_date"]
        verbose_name = "Task"
        verbose_name_plural = "Tasks"