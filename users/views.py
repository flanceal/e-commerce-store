from django.shortcuts import render, redirect
from .models import User
from .form import UserLoginForm, UserRegistrationForm
from django.contrib import auth
from django.urls import reverse


def login(request):
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
            return redirect(redirect('users:login'))
    form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'users/registration.html', context)
