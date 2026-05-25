from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Класс Пользователь"""

    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(
        max_length=11, verbose_name="Телефон", blank=True, null=True, help_text="Укажите номер телефона"
    )

    token = models.CharField(max_length=100, verbose_name="Token", blank=True, null=True)
    block_status = models.BooleanField(default=False, verbose_name="Статус блокировки пользователя")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [("can_block_user", "Can block user")]

    def __str__(self):
        return self.email
