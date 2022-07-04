from django.contrib import admin
from .models import FriendRequest, Message, User

# Register your models here.
admin.site.register(User)
admin.site.register(Message)
admin.site.register(FriendRequest)

