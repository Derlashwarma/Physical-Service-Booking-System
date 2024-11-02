from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import check_password
from register.models import CustomUser

# Create your views here.
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_worker:
                    return redirect('employee:employee_feed')
                else:
                    return redirect('employer:employer_feed')
            else:
                form.add_error('username', "Invalid username or password")
                return render(request,'login.html',{'form':form})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('landing:landing_page')
