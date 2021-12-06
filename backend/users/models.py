from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F, Q


class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=150, unique=True, blank=False)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    password = models.CharField(max_length=150)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower', verbose_name='Подписчик')
    following = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following', verbose_name='Автор')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'following'],
                                    name='unique_pair'),
            models.CheckConstraint(check=~Q(user=F('following')),
                                   name='forbidden_selfsubscribe'),
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.following}'
