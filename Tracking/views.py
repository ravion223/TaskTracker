from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.db.models import Q
from django.forms import BaseModelForm
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .mixins import UserIsOwnerMixin
from .models import Task, Comment, Profile, Workspace
from .forms import TaskCreationForm, TaskUpdateForm, TaskFilterForm, TaskCommentForm, ProfileUpdateForm, WorkspaceCreationForm


# Create your views here.

class WorkspacesListView(ListView):
    model = Workspace
    template_name = 'Tracking/main-page.html'
    context_object_name = 'workspaces'

    def get_queryset(self):
        return Workspace.objects.filter(Q(user=self.request.user) | Q(allowed_users=self.request.user)).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = None
        if self.request.user.is_authenticated:
            profile = get_object_or_404(Profile, user=self.request.user)

        context['profile'] = profile

        return context


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

    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if task.user != self.request.user and not task.workspace.allowed_users.filter(id=self.request.user.id).exists():
            raise Http404("You are not allowed to access this task.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = None
        if self.request.user.is_authenticated:
            profile = get_object_or_404(Profile, user=self.request.user)

        context['form'] = TaskCommentForm
        context['profile'] = profile
        return context


    def post(self, request, *args, **kwargs):
        form = TaskCommentForm(request.POST, request.FILES)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.task = self.get_object()
            comment.save()
            return redirect('task-detail', pk=comment.task.pk)
        else:
            raise ValidationError("Bad input")
        

class WorkspaceTasksView(View):
    template_name = 'Tracking/workspace-tasks.html'
    form_class = TaskFilterForm

    def dispatch(self, request, *args, **kwargs):
        workspace = get_object_or_404(Workspace, id=kwargs.get('workspace_id'))

        if workspace.user != self.request.user and not workspace.allowed_users.filter(id=self.request.user.id).exists():
            raise Http404("You are not allowed to access this workspace.")
        
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self, **kwargs):
        workspace = get_object_or_404(Workspace, id=kwargs.get('workspace_id'))
        queryset = workspace.tasks.all()

        status = self.request.GET.get('status', '')
        priority = self.request.GET.get('priority', '')

        if status:
            queryset = queryset.filter(status=status)

        elif priority:
            queryset = queryset.filter(priority=priority)

        return queryset

    def get(self, request, *args, **kwargs):
        workspace = get_object_or_404(Workspace, id=kwargs.get('workspace_id'))
        tasks = self.get_queryset(**kwargs)

        profile = None
        if self.request.user.is_authenticated:
            profile = get_object_or_404(Profile, user=self.request.user)

        context = {
            'workspace': workspace,
            'tasks': tasks,
            'profile': profile,
            'form': self.form_class
        }

        return render(
            request,
            self.template_name,
            context
        )

        

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
    

class SomeProfileDetailView(LoginRequiredMixin, View):
    model = Profile
    template_name = 'Tracking/some-profile.html'
    context_object_name = 'sprofile'

    def get(self, request, *args, **kwargs):
        profile = None
        if self.request.user.is_authenticated:
            profile = get_object_or_404(Profile, user=self.request.user)

        sprofile = get_object_or_404(Profile, id=kwargs.get('profile_id'))

        context = {
            'profile': profile,
            'sprofile': sprofile
        }

        return render(
            request,
            self.template_name,
            context
        )


class TaskCreateView(LoginRequiredMixin, View):
    template_name = 'Tracking/task-create.html'
    form_class = TaskCreationForm

    def get(self, request, *args, **kwargs):
        workspace = Workspace.objects.get(id=kwargs.get('workspace_id'))
        form = self.form_class()

        profile = None
        if self.request.user.is_authenticated:
            profile = get_object_or_404(Profile, user=self.request.user)

        context = {
            'workspace': workspace,
            'form': form,
            'profile': profile
        }
        return render(
            request,
            self.template_name,
            context
        )
    
    def post(self, request, *args, **kwargs):
        workspace = Workspace.objects.get(id=kwargs.get('workspace_id'))
        form = self.form_class(request.POST)
        context = {
            'workspace': workspace,
            'form': form
        }
        if form.is_valid():
            form.instance.user_id = self.request.user.id
            workspace_id = kwargs.get('workspace_id')
            workspace = Workspace.objects.get(id=workspace_id)
            task = form.save(commit=False)
            task.workspace = workspace
            task.save()
            # Add the task to the workspace's tasks
            workspace.tasks.add(task)
            return redirect('workspace-tasks-list', workspace_id=workspace_id)
        return render(
            request,
            self.template_name,
            context
        )

    # def form_valid(self, form: TaskCreationForm):
    #     form.instance.user_id = self.request.user.id
    #     return super().form_valid(form)


class WorkspaceCreateView(CreateView):
    model = Workspace
    template_name = 'Tracking/workspace-create.html'
    form_class = WorkspaceCreationForm
    
    def get_success_url(self) -> str:
        return reverse_lazy('workspace-tasks-list', kwargs={'workspace_id': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = None
        if self.request.user.is_authenticated:
            profile = get_object_or_404(Profile, user=self.request.user)

        context['profile'] = profile

        return context
    
    def form_valid(self, form):
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
        return HttpResponseRedirect(reverse_lazy('workspace-tasks-list', kwargs={'workspace_id': task.workspace.id}))


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
    

def add_user_to_workspace(request, workspace_id):
    workspace = Workspace.objects.get(id=workspace_id)
    profile = None
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user=request.user)
    
    if request.method == "POST":
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            workspace.allowed_users.add(user)
            return redirect('workspace-tasks-list', workspace_id=workspace_id)
        except User.DoesNotExist:
            error_message = 'User with the entered username does not exist.'
            return render(
                request,
                'Tracking/add-user-to-workspace.html',
                {'workspace': workspace, 'error_message': error_message, 'profile': profile}
            )
        
    return render(
        request,
        'Tracking/add-user-to-workspace.html',
        {'workspace': workspace, 'profile': profile}
    )


class RemoveUserFromWorkspaceView(View):
    def post(self, request, *args, **kwargs):
        workspace_id = kwargs.get('workspace_id')
        user_id = kwargs.get('user_id')

        workspace = get_object_or_404(Workspace, id=workspace_id)
        user = get_object_or_404(User, id=user_id)

        workspace.allowed_users.remove(user)

        return redirect('allowed-users-list', workspace_id=workspace_id)
    

class WorkspaceTasksKanbanBoardView(View):
    template_name = 'Tracking/kanban-board.html'

    def get(self, request, *args, **kwargs):
        workspace = get_object_or_404(Workspace, id=kwargs.get('workspace_id'))

        if workspace.user != self.request.user and not workspace.allowed_users.filter(id=self.request.user.id).exists():
            raise Http404("You are not allowed to access this workspace.")
        
        todo_tasks = workspace.tasks.filter(status='todo')
        in_progress_tasks = workspace.tasks.filter(status='in_progress')
        done_tasks = workspace.tasks.filter(status='done')

        profile = None
        if self.request.user.is_authenticated:
            profile = get_object_or_404(Profile, user=self.request.user)

        # Prepare the context data
        context = {
            'profile': profile,
            'workspace': workspace,
            'todo_tasks': todo_tasks,
            'in_progress_tasks': in_progress_tasks,
            'done_tasks': done_tasks
        }

        # Render the template with the context data
        return render(request, self.template_name, context)


def update_status(request, task_id, new_status):
    task = Task.objects.get(id=task_id)
    task.status = new_status
    task.save()
    return JsonResponse({'success': True})


class WorkspaceAllowedUsersView(View):
    model = Workspace
    template_name = 'Tracking/workspace-allowed-users.html'

    def dispatch(self, request, *args, **kwargs):
        workspace = get_object_or_404(Workspace, id=kwargs.get('workspace_id'))

        if workspace.user != self.request.user and not workspace.allowed_users.filter(id=self.request.user.id).exists():
            raise Http404("You are not allowed to access this workspace.")
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self, **kwargs):
        workspace = get_object_or_404(Workspace, id=kwargs.get('workspace_id'))
        queryset = workspace.allowed_users.all()

        return queryset
    
    def get(self, request, *args, **kwargs):
        workspace = get_object_or_404(Workspace, id=kwargs.get('workspace_id'))
        allowed_users_list = self.get_queryset(**kwargs)

        profile = None
        if self.request.user.is_authenticated:
            profile = get_object_or_404(Profile, user=self.request.user)

        context = {
            'workspace': workspace,
            'allowed_users_list': allowed_users_list,
            'profile': profile
        }

        return render(
            request,
            'Tracking/workspace-allowed-users.html',
            context
        )
    

def update_text(request, comment_id):
    if request.method == 'POST':
        new_text = request.POST.get('new_text')
        commentary = get_object_or_404(Comment, id=comment_id)
        commentary.content = new_text
        commentary.save()
        return JsonResponse({'message': 'Text updated successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})