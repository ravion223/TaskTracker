from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import Task
from .forms import TaskCreationForm

# Create your views here.


class TasksListView(ListView):
    model = Task
    template_name = 'Tracking/tasks-list.html'
    context_object_name = 'tasks'


class TasksDetailView(DetailView):
    model = Task
    template_name = 'Tracking/task-detail.html'
    context_object_name = 'task'


class TaskCreateView(CreateView):
    model = Task
    template_name = 'Tracking/task-create.html'
    form_class = TaskCreationForm
    success_url = reverse_lazy('tasks-list')