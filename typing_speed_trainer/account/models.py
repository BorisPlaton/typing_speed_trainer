from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.urls import reverse


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Создает обычного пользователя с его почтой и паролем.
        """
        if not email:
            raise ValueError('Должна быть предоставлена почта пользователя.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Создает супер пользователя с его почтой и паролем.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Супер пользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Супер пользователь должен иметь is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Модель пользователя."""

    email = models.EmailField('Почта', unique=True)
    username = models.CharField('Имя пользователя', max_length=16, validators=[UnicodeUsernameValidator()])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_absolute_url(self):
        return reverse('account:profile', args=[self.pk])


class Profile(models.Model):
    """Модель профиля пользователя."""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile', verbose_name='Пользователь'
    )
    photo = models.ImageField(
        'Фото пользователя', upload_to='profile_photos/%Y/%m/%d/', default='profile_photos/default.jpg'
    )

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
