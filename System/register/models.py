from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Avg
from ckeditor.fields import RichTextField
from rate.models import Rating

class CustomUser(AbstractUser):
    is_worker = models.BooleanField(default=False)
    professional_summary = RichTextField(blank=True)
    professional_experience = RichTextField(blank=True)
    key_skills = RichTextField(blank=True)
    social_contacts = RichTextField(blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.username
    
    def get_average_rating(self, rating_name):
        average_rating = Rating.objects.filter(to_user=self, name=rating_name).aggregate(Avg('score'))
        return average_rating['score__avg'] or 0
