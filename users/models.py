from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def get_by_natural_key(self, email):
        return self.get(email=email)


class User(AbstractBaseUser, PermissionsMixin):
    """Пользователь"""

    email = models.EmailField(unique=True, verbose_name="Адрес электронной почты")
    phone = models.CharField(
        max_length=16, verbose_name="Номер телефона", blank=True, null=True
    )
    tg_chat_id = models.CharField(
        max_length=40, verbose_name="Chat_ID в Телеграм", blank=True, null=True
    )
    avatar = models.ImageField(
        upload_to="avatars/", verbose_name="Аватар", blank=True, null=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
