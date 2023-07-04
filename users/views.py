from django.shortcuts import render, redirect
from .models import User
from .form import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.contrib import auth, messages
from django.contrib.auth.forms import PasswordChangeForm
from products.models import Basket
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from common.view import TitleMixin

from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView


class UserLoginView(TitleMixin, SuccessMessageMixin, LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    success_message = f"Welcome back"
    title = 'Store - Login'

    def get_success_url(self):
        return reverse_lazy('index')


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    success_message = f"Registration completed successfully"
    title = 'Store - Registration'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


class UserProfileView(TitleMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_message = 'Profile data were edited successfully'
    title = 'Store - Profile'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=[self.object.id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['baskets'] = Basket.objects.filter(user=self.object)
        return context


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')


class UserPasswordChangeView(TitleMixin, SuccessMessageMixin,PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = 'The password has changed successfully'
    title = 'Store - Password'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=[self.request.user.id])

