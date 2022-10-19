from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.urls import reverse


class CustomUserManager(BaseUserManager):
    """The manager class that swaps a username with an email."""

    def create_user(self, email, password=None, **extra_fields):
        """Creates an average user with his password and an email."""
        if not email:
            raise ValueError('Должна быть предоставлена почта пользователя.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Creates a superuser with his password and an email."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Супер пользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Супер пользователь должен иметь is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """The user model."""

    email = models.EmailField('Почта', unique=True)
    username = models.CharField('Имя пользователя', max_length=16, validators=[UnicodeUsernameValidator()])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_absolute_url(self):
        return reverse('account:profile', args=[self.pk])

    def delete_all_cached_results(self):
        """Deletes all user's cached results."""
        cache = CurrentUserCache()
        cache.user_id = self.pk
        cache.delete_all_user_results()


class Profile(models.Model):
    """The user's profile."""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile', verbose_name='Пользователь'
    )
    photo = models.ImageField(
        'Фото пользователя', upload_to='profile_photos/%Y/%m/%d/', default='profile_photos/default.jpg'
    )
    are_results_shown = models.BooleanField("Показывать последние результаты", default=True)
    is_email_shown = models.BooleanField("Показывать почту", default=False)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def get_absolute_url(self):
        return reverse('account:profile', args=[self.user.pk])

    def __str__(self):
        return f'{self.user}'
