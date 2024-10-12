from django.db import models
from django.contrib.auth.hashers import make_password

class Rating(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='ratings_given')  
    score = models.IntegerField()

    def __str__(self):
        return self.name

class User(models.Model):
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    username = models.CharField(max_length=100, blank=True, unique=True)
    password = models.CharField(max_length=100)
    is_worker = models.BooleanField(default=False)
    professional_summary = models.TextField(blank=True)
    professional_experience = models.TextField(blank=True)
    key_skills = models.TextField(blank=True)
    social_contacts = models.TextField(blank=True)
    ratings = models.ManyToManyField(Rating, blank=True, related_name='rated_users')
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    contact_number = models.IntegerField(blank=True, null=True)
    field_of_work = models.TextField(blank=True)
    previous_employment = models.TextField( blank=True)

    def __str__(self):
        return self.username
