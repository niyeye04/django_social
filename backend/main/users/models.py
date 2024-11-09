from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
# Create your models here.


class CustomUser(AbstractUser):
    gender_choices = [
        ("F", "Female"),
        ("M", "Male")
    ]

    phone_number = models.CharField(unique=True, max_length=15, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/users/', null=True, blank=True)
    birthdate = models.DateField(verbose_name="Birthday",  blank=True, null=True)
    bio = models.TextField(max_length=300, blank=True, null=True)
    gender = models.CharField(choices=gender_choices, max_length=1, default="M")
    followers = models.ManyToManyField('self', symmetrical=False, related_name="following", blank=True)


    def __str__(self):
        return f"{self.username}"
    
    @property
    def age(self):
        if self.birthdate:
           today = date.today()
           age = today.year - self.birthdate.year - (today.month,today.day)<(self.birthdate.month,self.birthdate.day)
           return age
        return  None
    
    #followers helper methods
    def follow(self,user):
        self.following.add(user)
    
    def unfollow(self,user):
        self.following.remove(user)

    def is_fllowing(self,user):
        return self.following.filter(id = user.id).exists()
    
    def is_followed_by(self, user):
        return self.followers.filter(id = user.id).exists()
    
    @property
    def followers_count(self):
        return self.followers.count()
    
    @property
    def following_count(self):
        return self.following.count()