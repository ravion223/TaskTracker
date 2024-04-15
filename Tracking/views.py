from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from .mixins import UserIsOwnerMixin
from .models import Task, Comment, Profile
from .forms import TaskCreationForm, TaskUpdateForm, TaskFilterForm, TaskCommentForm, ProfileUpdateForm


# Create your views here.

class TasksListView(ListView):
    model = Task
    template_name = 'Tracking/tasks-list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status', '')
        if status:
            queryset = queryset.filter(status=status)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = None
        if self.request.user.is_authenticated:
            profile = get_object_or_404(Profile, user=self.request.user)

        context['form'] = TaskFilterForm(self.request.GET)
        context['profile'] = profile

        return context


class TasksDetailView(DetailView):
    model = Task
    template_name = 'Tracking/task-detail.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = None
        if self.request.user.is_authenticated:
            profile = get_object_or_404(Profile, user=self.request.user)

        context['form'] = TaskCommentForm
        context['profile'] = profile
        return context


    def post(self, request, *args, **kwargs):
        form = TaskCommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.task = self.get_object()
            comment.save()
            return redirect('task-detail', pk=comment.task.pk)
        else:
            raise ValidationError("Bad input")
        

class MyProfileDetailView(LoginRequiredMixin, View):
    model = Profile
    template_name = 'Tracking/my-profile.html'
    context_object_name = 'myprofile'

    def get(self, request, *args, **kwargs):
        profile = None
        if self.request.user.is_authenticated:
            profile = get_object_or_404(Profile, user=self.request.user)

        context = {
            'profile': profile
        }

        return render(
            request,
            self.template_name,
            context
        )


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'Tracking/task-create.html'
    form_class = TaskCreationForm
    success_url = reverse_lazy('tasks-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = None
        if self.request.user.is_authenticated:
            profile = get_object_or_404(Profile, user=self.request.user)

        context['profile'] = profile

        return context

    def form_valid(self, form: TaskCreationForm):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)
    

class TaskDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('tasks-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = None
        if self.request.user.is_authenticated:
            profile = get_object_or_404(Profile, user=self.request.user)

        context['profile'] = profile
        
        return context


class TaskUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Task
    template_name = 'Tracking/task-update.html'
    form_class = TaskUpdateForm
    
    def get_success_url(self) -> str:
        return reverse_lazy('task-detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = None
        if self.request.user.is_authenticated:
            profile = get_object_or_404(Profile, user=self.request.user)

        context['profile'] = profile
        
        return context


class MyProfileUpdateView(UpdateView):
    model = Profile
    template_name = 'Tracking/profile-update.html'
    form_class = ProfileUpdateForm
    success_url = reverse_lazy('my-profile')

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = None
        if self.request.user.is_authenticated:
            profile = get_object_or_404(Profile, user=self.request.user)

        context['profile'] = profile
        
        return context

    def form_valid(self, form: ProfileUpdateForm):
        # form.instance.user_id = self.request.user.id
        return super().form_valid(form)

class TaskCompleteView(LoginRequiredMixin, UserIsOwnerMixin, View):
    def get_object(self):
        task_id = self.kwargs.get('pk')
        return get_object_or_404(Task, pk = task_id)
    
    def post(self, request, *args, **kwargs):
        task = self.get_object()
        task.status = 'done'
        task.save()
        return HttpResponseRedirect(reverse_lazy('tasks-list'))


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['content']

    def form_valid(self, form):
        comment = self.get_object()
        if comment.author == self.request.user:
            return super().form_valid(form)
        raise PermissionError('You dont have permissions')

    def get_success_url(self):
        return reverse_lazy('task-detail', kwargs={'pk': self.object.task.id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = None
        if self.request.user.is_authenticated:
            profile = get_object_or_404(Profile, user=self.request.user)

        context['profile'] = profile
        
        return context
    

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    
    def get_success_url(self):
        return reverse_lazy('task-detail', kwargs={'pk': self.object.task.id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = None
        if self.request.user.is_authenticated:
            profile = get_object_or_404(Profile, user=self.request.user)

        context['profile'] = profile
        
        return context