# chatbot/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from .utils import hash_value


class User(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.username


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, first_name="", last_name="", email=""):
        if not username:
            raise ValueError("Kullanıcı adı gereklidir.")
        if not email:
            raise ValueError("Email gereklidir.")
#-----------------------------------------------------------------------
        user = self.model(
            username=hash_value(username),  # Kullanıcı adı hashlenmiş olarak kaydedilir
            first_name=hash_value(first_name),  # Ad hashlenmiş olarak kaydedilir
            last_name=hash_value(last_name),  # Soyad hashlenmiş olarak kaydedilir
            email=hash_value(email),  # Email hashlenmiş olarak kaydedilir
            created_at=timezone.now()
        )
        user.set_password(password)  # Şifre zaten Django'nun hash fonksiyonu ile hashlenir -
        user.save(using=self._db)
#-------------------------------------------------------------------------------
        return user

