from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F, Q


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    ROLE_CHOICES = (
        (USER, 'user'),
        (ADMIN, 'admin'),
    )

    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=USER)

    class Meta:
        ordering = ['id']

    @property
    def is_admin(self):
        return self.role == 'admin'

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower', verbose_name='Подписчик')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following', verbose_name='Автор')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='unique_pair'),
            models.CheckConstraint(check=~Q(user=F('author')),
                                   name='forbidden_selfsubscribe'),
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
