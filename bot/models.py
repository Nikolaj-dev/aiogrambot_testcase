from django.db import models
from django.contrib.auth.models import User


class TelegramChat(models.Model):
    chat_id = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscribed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class CurrencyHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=32)
    name = models.CharField(max_length=128)
    rate = models.FloatField()
    date = models.CharField(max_length=64)
    inverseRate = models.FloatField()

    def __str__(self):
        return str(self.user.username) + " " + str(self.created_at)
