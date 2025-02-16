from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    reset_password_token = models.CharField(max_length=64, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
