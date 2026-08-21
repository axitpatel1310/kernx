from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    def __str__(self):
        return self.email
    
from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="profile")
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/",blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.user.email}'s Profile"
    
from django.db import models
from django.conf import settings

class Activity(models.Model):
    ACTIVITY_TYPES = [
        ("architecture_created", "Architecture Created"),
        ("architecture_updated", "Architecture Updated"),
        ("architecture_viewed", "Architecture Viewed"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="activities")
    activity_type = models.CharField(max_length=50,choices=ACTIVITY_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.email} - {self.activity_type}"