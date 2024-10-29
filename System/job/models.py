from django.db import models
from register.models import CustomUser
from ckeditor.fields import RichTextField
from django.utils import timezone

# Create your models here.
class Job(models.Model):
    employer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    job_type = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    description = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_done = models.BooleanField(default=False)
    budget = models.DecimalField(decimal_places=2, max_digits=100)
    location = models.CharField(max_length=100, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.pk is not None: 
            old_instance = Job.objects.get(pk=self.pk)
            if old_instance.is_done != self.is_done and self.is_done:
                self.finished_at = timezone.now()
            elif old_instance.is_done and not self.is_done:
                self.finished_at = None 

        super().save(*args, **kwargs)

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
