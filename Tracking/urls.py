from django.urls import path
from .views import TasksListView, TasksDetailView, TaskCreateView, TaskDeleteView


urlpatterns = [
    path('', TasksListView.as_view(), name='tasks-list'),
    path('task/<int:pk>/', TasksDetailView.as_view(), name='task-detail'),
    path('create-task/', TaskCreateView.as_view(), name='task-creation'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
]