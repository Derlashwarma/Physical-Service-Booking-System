from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

class Rating(models.Model):
    name = models.CharField(max_length=30)
    from_user = models.ForeignKey('register.CustomUser', on_delete=models.SET_NULL, related_name='ratings_given', null=True)  
    to_user = models.ForeignKey('register.CustomUser', on_delete=models.SET_NULL, related_name='ratings_received', null=True)
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Review(models.Model):
    from_user = models.ForeignKey('register.CustomUser', on_delete=models.SET_NULL, related_name='review_given', null=True)  
    to_user = models.ForeignKey('register.CustomUser', on_delete=models.SET_NULL, related_name='review_received', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    review = models.TextField()

    def __str__(self):
        return f'review by {self.from_user.username} to {self.to_user.username}'