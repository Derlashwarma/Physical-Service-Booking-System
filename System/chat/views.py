from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import *
from job.models import *
from register.models import *


@login_required(login_url="login:login")
def chat_index(request):
    user = request.user
    users = None
    if user.is_worker:
        applications = JobApplication.objects.filter(worker=user)    
        jobs = Job.objects.filter(id__in=applications.values('job'))
    
        # Get the employers of those jobs
        users = CustomUser.objects.filter(id__in=jobs.values('employer'))
    else:
        jobs = Job.objects.filter(employer=user)
        applications = JobApplication.objects.filter(job__in=jobs)
        users = CustomUser.objects.filter(id__in=applications.values('worker'))

    return render(request, 'chat_index.html', {'users': users})

@login_required(login_url="login:login")
def chat_conversation(request, username):
    conversation_name = '_'.join(sorted([username, request.user.username]))
    try:
        user = CustomUser.objects.get(username=username)
        conversation = Conversation.objects.get(conversation_name=conversation_name)
    except Conversation.DoesNotExist:
        conversation = Conversation.objects.create(conversation_name=conversation_name)
    except CustomUser.DoesNotExist:
        return HttpResponse("DOES NOT EXIST")
    
    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text:
            # Create the message
            Message.objects.create(
                conversation=conversation,
                author=request.user,
                message=message_text
            )
            return redirect('chat:conversation',username=username)

    messages = conversation.chat_messages.order_by('created_at')
    context = {
        'conversation': conversation,
        'messages': messages,
        'other_user': user,
    }
    return render(request, 'chat_conversation.html',context)