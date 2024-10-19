from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Avg

class Rating(models.Model):
    name = models.CharField(max_length=30)
    from_user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='ratings_given')  
    to_user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='ratings_received')
    score = models.IntegerField()

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    is_worker = models.BooleanField(default=False)
    professional_summary = models.TextField(blank=True)
    professional_experience = models.TextField(blank=True)
    key_skills = models.TextField(blank=True)
    social_contacts = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    contact_number = models.IntegerField(blank=True, null=True)
    field_of_work = models.TextField(blank=True)
    previous_employment = models.TextField( blank=True)

    def __str__(self):
        return self.username
    
    def get_average_rating(self, rating_name):
        average_rating = Rating.objects.filter(to_user=self, name=rating_name).aggregate(Avg('score'))
        return average_rating['score__avg'] or 0
