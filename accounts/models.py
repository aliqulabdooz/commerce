from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    GENDER_CHOICES = (
        ('fem', 'female'),
        ('mal', 'male'),
    )
    phone_number = models.CharField(blank=True, max_length=11)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=3, default='mal')

