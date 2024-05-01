from django.db import models
from django.contrib.auth.models import User
from web_app.models import Channel

# Create your models here.
class Question(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()

    def __str__(self):
        return f"User: {self.user.username}",\
               f"Body: {self.body}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()

    def __str__(self):
        return f"User: {self.user.username}",\
               f"Question: {self.question}",\
               f"Body: {self.body}"
