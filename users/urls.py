from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views


app_name = 'users'

urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("registration/", views.UserRegistrationView.as_view(), name="registration"),
    path("profile/<int:pk>", login_required(views.UserProfileView.as_view()), name='profile'),
    path("logout/", views.UserLogoutView.as_view(), name='logout'),
    path("password/", views.UserPasswordChangeView.as_view(), name='password-change'),
]
