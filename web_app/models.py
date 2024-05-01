from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Channel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=500)
    banner_image = models.ImageField(upload_to='images/', blank=True, null=True)

class Post(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=150)
    photo = models.ImageField(upload_to='images/', blank=True)
    video = models.FileField(upload_to='videos/', blank=True)
    body = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.ManyToManyField(User, related_name='likes', blank=True)
    dislike = models.ManyToManyField(User, related_name='dislikes', blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField()
    like = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    dislike = models.ManyToManyField(User, related_name='comment_dislikes', blank=True)
    
    def __str__(self):
        return self.body
    