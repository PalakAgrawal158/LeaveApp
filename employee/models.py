from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser,User

class CustomUser(AbstractUser):
    ROLE_CHOICES = [('employee','Employee'),
                    ('manager','Manager')]
    
    email= models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    contact_no = models.CharField(max_length=10)
    address = models.TextField(max_length=70)
    is_manager=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now =True)
    manager = models.ForeignKey('self', on_delete=models.SET_NULL,blank=True, null=True, related_name='employees')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name","last_name","password","contact_no","address","role"]

