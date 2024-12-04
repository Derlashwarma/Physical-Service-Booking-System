from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from job.models import *
from register.models import *
from django.db.models import Q


@login_required(login_url="login:login")
def chat_index(request):
    user = request.user
    users = None
    if user.is_worker:
        applications = JobApplication.objects.filter(worker=user)    
        jobs = Job.objects.filter(id__in=applications.values('job'))
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
        if not __get_mutual_connection(request.user, user):
            return render(request, 'access_errors.html', 
                          {'status':403, 'message':"You do not have any connection with this user"})
        conversation = Conversation.objects.get(conversation_name=conversation_name)
    except Conversation.DoesNotExist:
        conversation = Conversation.objects.create(conversation_name=conversation_name)
    except CustomUser.DoesNotExist:
            return render(request, 'access_errors.html', 
                          {'status':404, 'message':"User does not Exist"})
    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text:
            Message.objects.create(
                conversation=conversation,
                author=request.user,
                message=message_text
            )
            return redirect('chat:conversation', username=username)
    
    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text:
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

def __get_mutual_connection(from_user, to_user):
    if from_user.is_worker:
        return JobApplication.objects.filter(Q(worker=from_user, job__employer=to_user)).exists()
    elif not from_user.is_worker:
        return JobApplication.objects.filter(Q(worker=to_user, job__employer=from_user)).exists()
    return False