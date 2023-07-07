from datetime import timedelta
from http import HTTPStatus

from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from .models import EmailVerification, User


class UserRegistrationViewTestCase(TestCase):

    def setUp(self) -> None:
        self.path = reverse('users:registration')
        self.data = {
            'first_name': 'Danil', 'last_name': 'Fartanov',
            'username': 'fortflint', 'email': 'fortflint@gmail.com',
            'password1': 'checkpassword', 'password2': 'checkpassword'
        }

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.context_data['title'], 'Store - Registration')
        self.assertTemplateUsed(response, 'users/registration.html')

    def test_user_registration_post_success(self):
        # preparing all the data

        username = self.data['username']
        # checking if user with that username exists before creating
        self.assertFalse(User.objects.filter(username=username).exists())
        response = self.client.post(self.path, data=self.data)

        # checking creating user
        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=username).exists())

        # checking creating of email verification object
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())
        self.assertEquals(
            email_verification.first().expiration.date(),
            (now() + timedelta(hours=48)).date()
        )

    def test_user_registration_error(self):
        username = self.data['username']
        User.objects.create(username=username)
        response = self.client.post(self.path, self.data)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'A user with that username already exists.', html=True)


class UserLoginTestCase(TestCase):

    def setUp(self) -> None:
        self.path = reverse('users:login')
        self.login_data = {
            'username': "check",
            'password': 'heretest11'
        }
        self.wrong_login_data = {
            'username': "wrong_username",
            'password': 'wrong_password'
        }

    def test_login_get(self):
        response = self.client.get(self.path)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_post_successful(self):

        # creating object in User table
        hashed_password = make_password(self.login_data['password'])
        User.objects.create(username=self.login_data['username'], password=hashed_password)

        # login with that data
        response = self.client.post(self.path, self.login_data)

        # testing user login
        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('index'))

    def test_login_post_errors(self):

        # creating object in User table
        hashed_password = make_password(self.login_data['password'])
        User.objects.create(username=self.login_data['username'], password=hashed_password)

        # login with that data
        response = self.client.post(self.path, self.wrong_login_data)

        # testing errors
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Please enter a correct username and password")
