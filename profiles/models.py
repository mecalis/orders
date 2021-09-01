from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone

# Create your models here.

class DailyWaiter(models.Model):
    user = models.CharField(max_length=64)
    day = models.DateField(default=datetime.now, unique=False)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.created == None:
            self.created = timezone.now()
        return super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.user} - {self.day}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='nincs leírás')
    avatar = models.ImageField(upload_to='avatars', default='no_picture.png')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    email_confirmed = models.BooleanField(default=False)
    # last_post_seen = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    last_post_id = models.IntegerField(default=0, blank=True)
    default_boxes = models.BooleanField(default=True)

    def __str__(self):
        # return f"Profile of {self.user.username}"
        return self.user.username