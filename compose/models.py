from django.db import models
import uuid
from users.models import User
# Create your models here.

class Posts(models.Model):
    PRIVACY_OPTION = (
        ('public','public'),
        ('friends only','friends only'),
        ('only me', 'only me')
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    main_post = models.ForeignKey("posts", blank=True, null=True, related_name="main_compose", on_delete=models.CASCADE)
    post_body = models.TextField(null=True, blank=True)
    post_image = models.ImageField(null=True, blank=True, upload_to = 'images/')
    reposts = models.ManyToManyField("Posts", blank=True, related_name="repost")
    comments = models.ManyToManyField("Posts", blank=True, related_name="comment")
    blocked_users = models.ManyToManyField(User, blank=True, related_name="blocked_user")
    post_privacy = models.CharField(max_length=200, choices=PRIVACY_OPTION, default='public')
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.post_body[0:20] + ',' + str(self.post_image) + ',' + str(self.main_post)

    @property
    def reposted(self):
        queryset = self.reposts.all()
        return queryset

    @property
    def reposters(self):
        queryset = self.reposts.all().values_list('owner__id', flat=True)
        return queryset


    @property
    def likers(self):
        queryset = self.likedpost_set.all().values_list('likedby__id', flat=True)
        return queryset



class LikedPost(models.Model):
    likedby = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    
    def __str__(self):
        return self.likedby.username


