from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='nincs leírás')
    avatar = models.ImageField(upload_to='avatars', default='no_picture.png')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    email_confirmed = models.BooleanField(default=False)
    # last_post_seen = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    last_post_id = models.IntegerField(default=0, blank=True)

    def __str__(self):
        # return f"Profile of {self.user.username}"
        return self.user.username