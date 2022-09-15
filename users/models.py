from django.db import models

# Create your models here.

# users/models.py

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):

    email = models.EmailField(blank=False, max_length=254, verbose_name="email address")

    USERNAME_FIELD = "username"    
    EMAIL_FIELD    = "email"        
