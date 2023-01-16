from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Station(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name  # title


class Post(models.Model):

    stations = models.ForeignKey(Station, on_delete=models.PROTECT, default=0)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.stations  # title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

