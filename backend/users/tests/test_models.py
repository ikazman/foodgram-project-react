from django.contrib.auth import get_user_model
from django.test import TestCase
import django.core.exceptions as exceptions

User = get_user_model()


class ModelTests(TestCase):

    def test_create_user_with_valid_data_successfull(self):
        """Проверяем регистрацию пользователя с верными данными."""
        username = 'renton'
        password = 'begbie_psycho'
        email = 'markrenton@fake.mail'
        first_name = 'Mark'
        last_name = 'Renton'

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
