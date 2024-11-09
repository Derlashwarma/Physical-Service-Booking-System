from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Avg
from ckeditor.fields import RichTextField
from rate.models import Rating

class CustomUser(AbstractUser):
    is_worker = models.BooleanField(default=False)
    professional_summary = RichTextField()
    professional_experience = RichTextField()
    key_skills = RichTextField()
    social_contacts = RichTextField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    contact_number = models.IntegerField(blank=True, null=True)
    field_of_work = models.TextField(blank=True)
    previous_employment = models.TextField( blank=True)

    def __str__(self):
        return self.username
    
    def get_average_rating(self, rating_name):
        average_rating = Rating.objects.filter(to_user=self, name=rating_name).aggregate(Avg('score'))
        return average_rating['score__avg'] or 0
