from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Account(models.Model):
    account_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(User, related_name='accounts')

    def __str__(self):
        return self.account_name

class Event(models.Model):
    name = models.CharField(max_length=120)
    room_number = models.IntegerField()
    date = models.DateField()

    class Meta:
        unique_together = [['room_number', 'date']]

    def __str__(self):
        return f"{self.name} @ {self.room_number} on {self.date}"

class GameRecord(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    played_at = models.DateTimeField(auto_now_add=True)