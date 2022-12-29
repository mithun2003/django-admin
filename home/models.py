from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    movie = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    img = models.ImageField(default='',upload_to='post')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.movie
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    status = models.IntegerField(default=1)  
class Admin(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)  