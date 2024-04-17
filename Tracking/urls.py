from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import TasksListView, TasksDetailView, TaskCreateView, TaskDeleteView, TaskUpdateView, TaskCompleteView, CommentUpdateView, CommentDeleteView, MyProfileDetailView, MyProfileUpdateView, update_task_status


urlpatterns = [
    path('', login_required(TasksListView.as_view()), name='tasks-list'),
    path('task/<int:pk>/', login_required(TasksDetailView.as_view()), name='task-detail'),
    path('create-task/', login_required(TaskCreateView.as_view()), name='task-creation'),
    path('task/<int:pk>/delete/', login_required(TaskDeleteView.as_view()), name='task-delete'),
    path('task/<int:pk>/update/', login_required(TaskUpdateView.as_view()), name='task-update'),
    path('task/<int:pk>/complete/', login_required(TaskCompleteView.as_view()), name='task-complete'),
    path('comment/update/<int:pk>/', login_required(CommentUpdateView.as_view()), name='comment-update'),
    path('comment/delete/<int:pk>/', login_required(CommentDeleteView.as_view()), name='comment-delete'),
    path('my-profile/', MyProfileDetailView.as_view(), name='my-profile'),
    path('my-profile/update/', MyProfileUpdateView.as_view(), name='my-profile-update'),
    path('update_task_status/<int:pk>/<slug:status>/', update_task_status, name='update_task_status'),
]