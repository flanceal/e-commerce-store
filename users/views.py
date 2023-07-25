from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from common.view import TitleMixin
from products.models import Basket

from .forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from .models import EmailVerification, User


class UserLoginView(TitleMixin, SuccessMessageMixin, LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    success_message = "Welcome back"
    title = 'Store - Login'

    def get_success_url(self):
        return reverse_lazy('index')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        user = User.objects.get(username=username)
        if not user.is_verified_email:
            messages.error(self.request, "Please verify your email before logging in.")
            return self.form_invalid(form)

        return super().form_valid(form)


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    success_message = "Registration completed successfully. Please confirm your email"
    title = 'Store - Registration'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


def _get_form(request, formcls, prefix):
    data = request.POST if prefix in request.POST else None
    return formcls(data, prefix=prefix)


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


class UserPasswordChangeView(TitleMixin, SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = 'The password has changed successfully'
    title = 'Store - Password'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=[self.request.user.id])


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Store - Email verification'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return redirect('index')
