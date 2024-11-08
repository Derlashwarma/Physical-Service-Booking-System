from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="login:login")
def chat_index(request, chat_room=None):
    context = {
        'room_name':chat_room
    }
    return render(request, 'chat_index.html', context)
