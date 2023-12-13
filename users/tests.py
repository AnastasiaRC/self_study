from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User


class UserTestCase(APITestCase):

    def setUp(self):
        self.maxDiff = None
        self.user = User.objects.create(
            email="test@yandex.by",
            first_name="test",
            last_name="test",
            role="AUTHOR",
            is_superuser=False,
            is_staff=False,
            is_active=True,
        )

        self.user.set_password("test")
        self.user.save()

        token = RefreshToken.for_user(self.user)
        self.access_token = str(token.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_register_user(self):
        """Тестирование регистрации пользователя (правильный пароль)"""
        data = {
            "email": "test3@yandex.by",
            "password": "1234567",
            "password2": "1234567",
            "first_name": "Test",
            "last_name": "Test",
        }

        response = self.client.post(reverse('users:users_registration'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(2, User.objects.all().count())

    def test_register_user_error(self):
        """Тестирование регистрации пользователя (неправильный пароль)"""
        data = {
            "email": "test3@yandex.by",
            "password": "1234567",
            "password2": "0",
            "first_name": "Test2",

        }

        response = self.client.post(reverse('users:users_registration'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user(self):
        """Тестированеи обновления профиля пользователя"""
        data = {
            "email": self.user.email,
            "password": "test",
            "password2": "test",
            "first_name": "Test_up",
            "last_name": self.user.last_name,
        }

        response = self.client.put(reverse("users:users_update", args=(self.user.pk,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, data['first_name'])

    def test_delete_user(self):
        """Тестирование удаления профиля пользователя"""
        response = self.client.delete(reverse("users:users_delete", args=(self.user.pk,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(0, User.objects.all().count())
