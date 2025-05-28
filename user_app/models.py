from django.apps import apps
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from datetime import timedelta
from datetime import datetime



class UserManager(BaseUserManager):
    def create_user(self, email=None, password=None):
        if not email:
            raise ValueError('Необходимо указать email!')
        if User.objects.filter(email=email).exists():
            raise ValueError('Пользователь с таким email уже существует.')
        user = self.model(email=email)
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_user_staff(self, email=None, password=None):
        """
        Создание сотрудников для клиник, с паролем.
        """
        if not email:
            raise ValueError('Необходимо указать email!')
        if not password:
            raise ValueError('Необходимо указать пароль для сотрудника или партнера клиники!')

        user_staff = self.model(email=email)
        # Устанавливаем пароль через метод set_password
        user_staff.set_password(password)
        user_staff.is_staff = True
        user_staff.is_active = True  # Обязательно активируем сотрудника
        user_staff.save(using=self._db)
        return user_staff

    def create_superuser(self, email=None, password=None):
        """
        Создание суперпользователя с обязательным паролем.
        """
        if not email:
            raise ValueError('Необходимо указать email!')
        if not password:
            raise ValueError('Необходимо указать пароль для суперпользователя!')

        # Создаем пользователя без пароля
        user = self.model(email=email)
        # Устанавливаем пароль через метод set_password
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True  # Обязательно активируем суперпользователя
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    USER_ROLE = [
        ('user', 'USER'),
        ('superuser', 'SUPERUSER'),
        ('doc', 'DOC'),
    ]

    email = models.EmailField(unique=True, verbose_name='email')
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=25, choices=USER_ROLE, default='user')


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def str(self):
        return str(self.email)

    class Meta:
        indexes = [
            models.Index(fields=['email']),
        ]


class SMSVerification(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=4, verbose_name='Код')
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f'email Пользователя: {self.email} Код: {self.code}'

    def is_code_valid(self):
        return (
                not self.is_used and
                timezone.now() < self.created_at + timedelta(minutes=3)
        )

    class Meta:
        indexes = [
            models.Index(fields=['email', 'code', 'created_at']),
        ]



# Запись к врачу
# Запись на прием
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтвержден'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
    ]







