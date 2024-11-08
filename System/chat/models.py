from django.db import models
from register.models import CustomUser

class Conversation(models.Model):
    conversation_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.conversation_name
    
class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='chat_messages', on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    message = models.CharField(max_length=500, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username} : {self.message}'