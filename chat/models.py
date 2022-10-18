from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

class User(AbstractUser):
    image = models.ImageField(upload_to='users', default='default.jpg')
    
    def __str__(self):
        return self.username

class Message(models.Model):
    owner = models.ForeignKey(
        get_user_model(), 
        on_delete=models.CASCADE
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.owner.username

    def get_last_10_msgs(self):
        return Message.objects.order_by('-created_at').all[10]
