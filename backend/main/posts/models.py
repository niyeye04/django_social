from django.db import models
from users.models import CustomUser as User
from datetime import datetime, timedelta
from django.utils.timezone import now
from groups.models import Group

# Create your models here.
class Post(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE, related_name="posts")
    content = models.ImageField(upload_to='posts/', default=None)
    #group = models.ForeignKey("groups.Group", on_delete=models.CASCADE,blank=True,related_name="posts", null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group_posts", blank=True, null=True)  # Nullable, links to a group if it's a group post
    caption = models.CharField(max_length=200, blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User,related_name="liked_posts",blank=True)
    dislikes = models.ManyToManyField(User,related_name="disliked_posts",blank=True)

    @property
    def is_group_post(self):
        if self.group is None:
            return False
        return True

    @property
    def like_count(self):
        return self.likes.count()
    
    @property
    def dislike_count(self):
        return self.dislikes.count()
    
    def __str__(self):
        return f"Posted by {self.owner.username}"
    
    @property
    def time_since_posted(self):
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

class Comments(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name="comments")
    owner = models.ForeignKey(User,on_delete=models.CASCADE, related_name="commenter")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Commented by {self.owner.username} at {self.created_at}" 
    
    @property
    def time_since_posted(self):
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