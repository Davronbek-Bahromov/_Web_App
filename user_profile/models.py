from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    phone = models.CharField(max_length=13)
    photo = models.ImageField(upload_to='images/', blank=True, null=True)
    follows = models.ManyToManyField('self', symmetrical=False, related_name='followed_by', blank=True)
    bio = models.TextField()
    twitter_link = models.CharField(max_length=155)
    instagram_link = models.CharField(max_length=155)
    facebook_link = models.CharField(max_length=155)
    telegram_link = models.CharField(max_length=155)
    pinterest_link = models.CharField(max_length=155)

    def __str__(self):
        return self.name.username

def create_profile(sender, instance, created, **kwargs):
    if created:
        if not hasattr:
            user_profile = UserProfile(name=instance)
            user_profile.save()
            user_profile.follows.set([instance.userprofile.id])
            user_profile.save()
            

post_save.connect(create_profile, sender=User)