import random

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    reset_password_token = models.CharField(max_length=64, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)

    def generate_verification_code(self):
        """Genera un codigo para verificar el email"""
        self.verification_code = str(random.randint(100000,999999))
        self.save()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
