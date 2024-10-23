from django.db import models
from register.models import CustomUser
from ckeditor.fields import RichTextField

# Create your models here.
class Job(models.Model):
    employer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_done = models.BooleanField(default=False)
    budget = models.DecimalField(decimal_places=2, max_digits=100)

    def __str__(self):
        return self.title
    
    def get_short_description(self):
        return self.description[:500] or None
    
class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined')
    ]

    job = models.ForeignKey(Job, on_delete= models.CASCADE)
    worker = models.ForeignKey(CustomUser, on_delete= models.CASCADE)
    status = models.CharField(max_length=10, choices= STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Application by {self.worker} for {self.job}'
