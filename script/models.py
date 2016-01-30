from django.db import models

class User(models.Model):
    username = models.TextField(unique=True)
    password = models.TextField()
    active = models.BooleanField()
    health = models.IntegerField()

class Item(models.Model):
    itemType = models.TextField()
    count = models.IntegerField()
    handable =models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
