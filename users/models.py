from django.db import models

# Create your models here.

# users/models.py

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):

    email = models.EmailField(blank=False, max_length=254, verbose_name="email address")

    USERNAME_FIELD = "username"    
    EMAIL_FIELD    = "email"     
    
class UserRoles(models.Model):
    
    class Roles(models.TextChoices):
        PMU             = 'PMU', _('PMU')
        PROVIDER_ADMIN  = 'PRA', _('Provider_admin')
        PROVIDER        = 'PR', _('Provider')
        CONSUMER        = 'CR', _('Consumer')

    username       = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    org_id         = models.CharField(max_length=100)
    role           = models.CharField(max_length=50, choices=Roles.choices, default=Roles.CONSUMER)
    
  
 
