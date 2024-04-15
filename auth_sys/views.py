from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sign-in')
    else:
        form = SignUpForm()
    
    return render(
        request,
        'auth_sys/register-form.html',
        {'form': form}
    )


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            else:
                messages.error(request, "Wrong username or password")

            return redirect('tasks-list')
    else:
        form = AuthenticationForm()
    
    return render(
        request,
        'auth_sys/login-form.html',
        {'form': form}
    )


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')