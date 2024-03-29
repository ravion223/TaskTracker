from django.urls import path
from .views import TasksListView, TasksDetailView, TaskCreateView


urlpatterns = [
    path('', TasksListView.as_view(), name='tasks-list'),
    path('task/<int:pk>/', TasksDetailView.as_view(), name='task-detail'),
    path('create-task/', TaskCreateView.as_view(), name='task-creation')
]