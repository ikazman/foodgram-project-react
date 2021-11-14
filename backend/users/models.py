from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    ROLE_CHOICES = (
        (USER, 'user'),
        (ADMIN, 'admin'),
    )

    username = models.CharField('Имя пользователя',
                                max_length=150, unique=True)
    password = models.CharField('Пароль',
                                max_length=150)
    email = models.EmailField('Электронная почта',
                              max_length=254, unique=True)
    first_name = models.CharField('Имя',
                                  max_length=150)
    last_name = models.CharField('Фамилия',
                                 max_length=150)
    role = models.CharField('Роль пользователя',
                            max_length=20, choices=ROLE_CHOICES, default=USER)

    class Meta:
        ordering = ['username']

    @property
    def is_admin(self):
        return self.role == 'admin'

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower',
                             verbose_name='Подписчик')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following',
                               verbose_name='Автор')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='unique_pair'),
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
