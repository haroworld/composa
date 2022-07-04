from distutils.command.upload import upload
from urllib import request
from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
import uuid

from django.dispatch import receiver


# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    username = models.CharField(max_length=200, unique=True)
    bio = models.TextField(null=True,blank=True)
    location = models.CharField(max_length=200)
    dob = models.DateField(max_length=10, null=True)
    friends = models.ManyToManyField("User", related_name='friend',blank=True)
    blocked = models.ManyToManyField("User", blank=True, related_name="block_user")
    sent_requests = models.ManyToManyField("User", related_name='sent_request', blank=True)
    received_requests = models.ManyToManyField("User", related_name='received_request', blank=True)
    profile_image = models.ImageField(blank=True,null=True,upload_to='images/profiles/', default="images/profiles/user-default.png")
    online = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    


class FriendRequest(models.Model):
    sender = models.ForeignKey(User,  related_name='senders', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User,related_name='receivers', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.sender.username + ',' + str(self.receiver.username)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, related_name='msg_receiver')
    image = models.ImageField(null=True,blank=True, upload_to = 'images/message_media/')
    body = models.TextField(null=True,blank=True)
    replies = models.ManyToManyField("Message", related_name='reply',blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)


    def __str__(self):
        return self.body[0:10] + ',' + str(self.image)
    
    class Meta:
        ordering = ['-created']