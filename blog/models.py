from django.db import models

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=100)
    
