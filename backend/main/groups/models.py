from django.db import models
from users.models import CustomUser as User
# from posts.models import Post
from datetime import datetime, timedelta
from django.utils.timezone import now


# Create your models here.
class Group(models.Model):
    admin =  models.ManyToManyField(User,related_name="admins",blank=True)
    members = models.ManyToManyField(User,related_name="members",blank=True)
    # posts =  models.ForeignKey(Post, on_delete=models.CASCADE, related_name="posts", blank=True, null=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    profile_pic =  models.ImageField(upload_to="profile_pics/group/",null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def members_count(self):
        return self.members.count()
    
    @property
    def admins_count(self):
        return self.admins.count()
    
    @property
    def time_since_created(self):
        time_diff = now() - self.created_at
        seconds = time_diff.total_seconds()

        if seconds < 60:
            return f"{int(seconds)} seconds ago"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif seconds < 86400:
            hours = int(seconds // 3600)
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif seconds < 2592000:
            days = int(seconds // 86400)
            return f"{days} day{'s' if days != 1 else ''} ago"
        elif seconds < 31536000:
            months = int(seconds // 2592000)
            return f"{months} month{'s' if months != 1 else ''} ago"
        else:
            years = int(seconds // 31536000)
            return f"{years} year{'s' if years != 1 else ''} ago"
    
    def __str__(self):
        return self.name