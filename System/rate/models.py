from django.db import models

class Rating(models.Model):
    name = models.CharField(max_length=30)
    from_user = models.ForeignKey('register.CustomUser', on_delete=models.SET_NULL, related_name='ratings_given', null=True)  
    to_user = models.ForeignKey('register.CustomUser', on_delete=models.SET_NULL, related_name='ratings_received', null=True)
    score = models.IntegerField()

    def __str__(self):
        return self.name
