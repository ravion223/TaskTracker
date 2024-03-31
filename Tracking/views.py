from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Task
from .forms import TaskCreationForm, TaskUpdateForm

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

    def form_valid(self, form: TaskCreationForm):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)
    

class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy('tasks-list')


class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'Tracking/task-update.html'
    form_class = TaskUpdateForm
    
    def get_success_url(self) -> str:
        return reverse_lazy('task-detail', kwargs={'pk': self.object.pk})