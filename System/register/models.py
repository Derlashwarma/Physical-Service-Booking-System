from django.db import models
from django.contrib.auth.hashers import make_password

class User(models.Model):
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=100, blank=True, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username