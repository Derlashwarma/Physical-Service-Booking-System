from django.db import models
from django.contrib.auth.models import AbstractUser

class Rating(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='ratings_given')  
    score = models.IntegerField()

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Custom related name
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Custom related name
        blank=True,
        help_text='Specific permissions for this user.'
    )
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
