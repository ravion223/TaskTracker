from django.urls import path
from .views import register_view, login_view, logout_view

urlpatterns = [
    path('authentication/register/', register_view, name='registration'),
    path('authentication/login/', login_view, name='sign-in'),
    path('authentication/logout/', logout_view, name='logout'),
]