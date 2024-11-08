from django.urls import path
from .views import *

app_name="chat"

urlpatterns = [
    path('', chat_index, name='chat_index'),
    path('<str:username>', chat_conversation, name='conversation'),
    path('conversation/<str:username>/send/', chat_conversation, name='send_message'),
]
