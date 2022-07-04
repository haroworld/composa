from django.contrib import admin

from compose.models import LikedPost, Posts

# Register your models here.
admin.site.register(Posts)
admin.site.register(LikedPost)
