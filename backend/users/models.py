from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, RegexValidator
from django.db import models

from recipes.constants import (MAX_LEN_EMAIL, MAX_LEN_NAME,
                               USERNAME_FIELD_CONST, REQUIRED_FIELDS_CONST)


class User(AbstractUser):
    USERNAME_FIELD = USERNAME_FIELD_CONST
    REQUIRED_FIELDS = REQUIRED_FIELDS_CONST

    username = models.CharField(
        verbose_name='Username',
        max_length=MAX_LEN_NAME,
        unique=True,
        help_text='Enter username',
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9]+([_.-]?[a-zA-Z0-9])*$',
                message=('Only numbers, latin letters, '
                         'underscore, dash, dote. '
                         'Marks should not be at beginning.')
            )]
    )
    email = models.EmailField(
        verbose_name='User email',
        max_length=MAX_LEN_EMAIL,
        unique=True,
        validators=[EmailValidator],
        help_text='Enter user email'
    )
    first_name = models.CharField(
        verbose_name='User first name',
        max_length=MAX_LEN_NAME,
        help_text='Enter user first name'
    )
    last_name = models.CharField(
        verbose_name='User last name',
        max_length=MAX_LEN_NAME,
        help_text='Enter user last name'
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('username',)

    def __str__(self) -> str:
        return f'{self.username}: {self.email}'


class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        related_name='followed_users',
        on_delete=models.CASCADE,
        verbose_name='Follower',
    )
    author = models.ForeignKey(
        to=User,
        related_name='author',
        on_delete=models.CASCADE,
        verbose_name='Author',
    )

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'),
                name=(
                    '\n%(app_label)s_%(class)s user cannot subscribe '
                    'to same author twice\n'),
            ),
        )

    def __str__(self):
        return f'User {self.user} subscribed to {self.author}'

    def save(self, *args, **kwargs):
        if self.user == self.author:
            raise ValidationError('You cannot subscribe to yourself')
        super().save(*args, **kwargs)
