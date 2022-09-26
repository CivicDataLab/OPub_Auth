from django.db import models

# Create your models here.

# users/models.py

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):

    email = models.EmailField(blank=False, max_length=254, verbose_name="email address")

    USERNAME_FIELD = "username"    
    EMAIL_FIELD    = "email"     
    
class permissions(models.Model):
  
    roles = [
        ('EDITOR', 'Editor'),
        ('OWNER', 'Owner'),
        ('VIEWER', 'Viewer'),
    ]  
    user_name      = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    dataset_id     = models.CharField(max_length=100)
    resource_id    = models.CharField(max_length=100)
    role           = models.CharField(max_length=50,   max_length=2, choices=roles, default='VIEWER')
    columns        = models.JSONField()
    rows           = models.IntegerField()
 
