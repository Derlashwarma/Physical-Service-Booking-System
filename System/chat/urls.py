from django.urls import path
from .views import chat_index

app_name="chat"

urlpatterns = [
    path('<str:chat_room>', chat_index, name='chat_index'),
    path('', chat_index, name='chat_index_default')
]
