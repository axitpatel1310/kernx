from django.conf import settings
from django.db import models


class ArchitectureType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


import uuid

class Architecture(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    type = models.ForeignKey(ArchitectureType, on_delete=models.CASCADE, related_name="architectures")
    slug = models.SlugField()
    title = models.CharField(max_length=255)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)


class UserArchitecture(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    original = models.ForeignKey(Architecture,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=255)
    data = models.JSONField()
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.user} - {self.name}"
    
class TechnologyCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    def __str__(self):
        return self.name
    
class Technology(models.Model):
    category = models.ForeignKey(TechnologyCategory,on_delete=models.CASCADE,related_name="technologies",)
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    logo = models.ImageField(upload_to="technologies/", blank=True)
    class Meta:
        unique_together = ("category", "slug")
    def __str__(self):
        return self.name
    
class ProjectField(models.Model):
    name = models.CharField(max_length=100)
    key = models.SlugField(unique=True)
    FIELD_TYPES = [
        ("text", "Text"),
        ("number", "Number"),
        ("select", "Select"),
    ]
    field_type = models.CharField(max_length=20,choices=FIELD_TYPES)
    required = models.BooleanField(default=True)