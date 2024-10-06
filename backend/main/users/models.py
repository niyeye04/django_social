from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
# Create your models here.

class CustomUser(AbstractUser):
    phone_number = models.CharField(unique=True, max_length=15, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/users/', null=True, blank=True)
    birthdate = models.DateField(verbose_name="Birthday",  blank=True, null=True)
    bio = models.TextField(max_length=300, blank=True, null=True)
    
    def __str__(self):
        return f"{self.username}"
    
    @property
    def age(self):
        if self.birthdate:
           today = date.today()
           age = today.year - self.birthdate.year - (today.month,today.day)<(self.birthdate.month,self.birthdate.day)
           return age
        return  None