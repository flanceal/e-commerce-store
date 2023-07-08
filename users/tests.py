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
            'first_name': 'FirstName', 'last_name': 'LastName',
            'username': 'check', 'email': 'fortflint@gmail.com',
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

    def _create_user(self):
        hashed_password = make_password(self.login_data['password'])
        User.objects.create(username=self.login_data['username'], password=hashed_password)

    def test_login_get(self):
        response = self.client.get(self.path)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_post_successful(self):

        # creating object in User table
        self._create_user()

        # login with that data
        response = self.client.post(self.path, self.login_data)

        # testing user login
        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('index'))

    def test_login_post_errors(self):

        # creating object in User table
        self._create_user()

        # login with that data
        response = self.client.post(self.path, self.wrong_login_data)

        # testing errors
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Please enter a correct username and password")


class UserProfileTestCase(TestCase):

    def setUp(self) -> None:
        self.data = {
            'first_name': 'FirstName', 'last_name': 'LastName',
            'username': 'check', 'email': 'fortflint@gmail.com',
            'password': 'checkpassword'
        }

    def _create_user(self):
        hashed_password = make_password(self.data['password'])
        User.objects.create(
            first_name=self.data['first_name'], last_name=self.data['last_name'],
            username=self.data['username'], email=self.data['email'],
            password=hashed_password)

    def _login_into_account(self):
        login_page = reverse('users:login')
        self.client.post(login_page, data={
            'username': self.data['username'],
            'password': self.data['password']
        })

    @staticmethod
    def _get_profile_path():
        return reverse('users:profile', args=[User.objects.last().id])

    def test_user_profile_get(self):
        self._create_user()
        self._login_into_account()
        # check profile data
        response = self.client.get(self._get_profile_path())
        # extracting initial data in forms
        user_profile_data = response.context_data['form'].initial
        del user_profile_data['image']
        self.assertTrue(set(user_profile_data.items()).issubset(set(self.data.items())))

    def test_user_profile_data_change(self):
        self._create_user()
        self._login_into_account()
        # checking changes in user profile
        response = self.client.post(self._get_profile_path(), {'first_name': "NewFirstName"})
        new_user_data_displayed = response.context_data['form'].initial
        new_db_user_data = response.context_data['user']
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(new_user_data_displayed['first_name'], "NewFirstName")
        self.assertEquals(new_db_user_data.first_name, "NewFirstName")
