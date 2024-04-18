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
    workspace = models.ForeignKey('Workspace', on_delete=models.CASCADE, related_name='task_set', blank=True, null=True)

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


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"comment to {self.task.title} by {self.author}"
    
    class Meta:
        ordering = ['created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profiles')

    name_surname = models.CharField(max_length=63, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    profile_pic = models.ImageField(blank=True, null=True, upload_to="profile/")
    created_at = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f'profile of {self.user.username}'
    

class Workspace(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workspaces')
    tasks = models.ManyToManyField(Task, related_name='workspaces', blank=True)
    allowed_users = models.ManyToManyField(User, related_name='allowed_workspace', blank=True)

    title = models.CharField(max_length=63)

    def __str__(self) -> str:
        return f"Workspace {self.title} - {self.user.username}"