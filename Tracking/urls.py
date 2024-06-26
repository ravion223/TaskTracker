from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import TasksListView, TasksDetailView, TaskCreateView, TaskDeleteView, TaskUpdateView, TaskCompleteView, CommentUpdateView, CommentDeleteView, MyProfileDetailView, MyProfileUpdateView, WorkspacesListView, WorkspaceCreateView, WorkspaceTasksView, add_user_to_workspace, WorkspaceTasksKanbanBoardView, update_status, WorkspaceAllowedUsersView, update_text, SomeProfileDetailView, RemoveUserFromWorkspaceView


urlpatterns = [
    path('', login_required(WorkspacesListView.as_view()), name='main-page'),
    path('workspace/create', login_required(WorkspaceCreateView.as_view()), name='workspace-creation'),
    path('workspace/<int:workspace_id>/tasks', login_required(WorkspaceTasksView.as_view()), name='workspace-tasks-list'),
    path('task/<int:pk>/', login_required(TasksDetailView.as_view()), name='task-detail'),
    path('workspace/<int:workspace_id>/task/create', login_required(TaskCreateView.as_view()), name='task-creation'),
    path('task/<int:pk>/delete/', login_required(TaskDeleteView.as_view()), name='task-delete'),
    path('task/<int:pk>/update/', login_required(TaskUpdateView.as_view()), name='task-update'),
    path('task/<int:pk>/complete/', login_required(TaskCompleteView.as_view()), name='task-complete'),
    path('comment/update/<int:pk>/', login_required(CommentUpdateView.as_view()), name='comment-update'),
    path('comment/delete/<int:pk>/', login_required(CommentDeleteView.as_view()), name='comment-delete'),
    path('my-profile/', login_required(MyProfileDetailView.as_view()), name='my-profile'),
    path('profile/<int:profile_id>/', login_required(SomeProfileDetailView.as_view()), name='some-profile'),
    path('my-profile/update/', login_required(MyProfileUpdateView.as_view()), name='my-profile-update'),
    path('workspace/<int:workspace_id>/add-user/', login_required(add_user_to_workspace), name='add-user-to-workspace'),
    path('workspace/<int:workspace_id>/kanban-board-tasks/', login_required(WorkspaceTasksKanbanBoardView.as_view()), name='kanban-board'),
    path('update_status/<int:task_id>/<str:new_status>/', update_status, name='update_status'),
    path('workspace/<int:workspace_id>/allowed-users/', login_required(WorkspaceAllowedUsersView.as_view()), name='allowed-users-list'),
    path('update-text/<int:comment_id>/', login_required(update_text), name='update-comment-text'),
    path('workspace/<int:workspace_id>/user/<int:user_id>/delete/', login_required(RemoveUserFromWorkspaceView.as_view()), name='remove-user-from-workspace')
]