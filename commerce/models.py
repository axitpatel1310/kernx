from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

class digital_products(models.Model):
    type = (
        ('Course','Course'),
        ('E_book','E_book'),
        ('Cheatsheet','Cheatsheet'),
        ('Quick_Guide','Quick_Guide'),
    )
    name = models.CharField(max_length=50)
    type_of = models.CharField(max_length=50,choices=type)
    price = models.FloatField()
    description = CKEditor5Field("Description")
    img = models.ImageField(upload_to="media")
    rating = models.FloatField(default=None)
    duration = models.DurationField(default=None)
    link = models.URLField(max_length=200, default="None")
    def __str__(self):
        return self.name