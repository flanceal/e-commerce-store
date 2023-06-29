from django.shortcuts import render, redirect
from .models import User
from .form import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.contrib import auth, messages
from django.contrib.auth.forms import PasswordChangeForm

from django.urls import reverse
from django.contrib.auth.decorators import login_required


def login(request):
    if request.user.is_authenticated:
        return redirect('users:profile')
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password'] 
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return redirect("index")
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration completed successfully')
            return redirect('users:login')
        else:
            return render(request, 'users/registration.html', {"form": form})
    form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'users/registration.html', context)


@login_required(login_url='users:login')
def profile(request):
    if request.method == "POST":
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=request.user)
    context = {'title': 'Your profile',  "form": form}
    return render(request, 'users/profile.html', context)


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect('index')
    messages.info(request, "You are not signed in")
    return redirect('users:login')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            auth.update_session_auth_hash(request, user)
            messages.success(request, 'Password has been changed successfully!')
            return redirect('users:login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "users/change_password.html", {'form': form})

