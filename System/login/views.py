from django.shortcuts import render, HttpResponse, redirect
from .forms import LoginForm
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from register.models import User

# Create your views here.
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            try:
                user = User.objects.get(username=username)
                if user is not None and check_password(password, user.password):
                    request.session['username'] = user.username
                    request.session['id'] = user.id
                    return HttpResponse("Logged in")
                else:
                    error = "invalid credintials"
                    form = LoginForm()
                    return render(request, 'login.html',{'error': error, 'form':form} )
            except Exception:
                form.add_error(None, 'Something happend bad')    
    else:
        form = LoginForm()
    return render(request,'login.html', {'form':form})