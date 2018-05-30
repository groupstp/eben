from django.conf import settings
from django.db import models


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True)
    entry = models.TextField()

    def __str__(self):
        return self.title
