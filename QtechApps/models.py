from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserSearchHistory(models.Model):
    searchKeyWords = models.CharField(max_length=50)
    createdTime = models.DateTimeField('date created', default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' % (self.searchKeyWords, self.owner)