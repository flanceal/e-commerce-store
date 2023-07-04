from django.shortcuts import render, redirect
from .models import User
from .form import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.contrib import auth, messages
from django.contrib.auth.forms import PasswordChangeForm
from products.models import Basket
from django.views.generic.edit import CreateView, UpdateView

from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('index')


class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Store - Registration'
        return context


class UserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=[self.object.id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Store - Profile'
        context['baskets'] = Basket.objects.filter(user=self.object)
        return context


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'users/change_password.html'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=[self.request.user.id])

