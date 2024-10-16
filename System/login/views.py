from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from register.models import CustomUser

# Create your views here.
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            try:
                user = CustomUser.objects.get(username=username)
                if user is not None and check_password(password, user.password):
                    request.session['username'] = user.username
                    request.session['id'] = user.id
                    login(request, user)

                    print(request.user.is_authenticated)
                    
                    if user.is_worker:  
                        return redirect('employee:employee_feed') 
                    else:
                        return redirect('employer:employer_feed') 
                else:
                    form.add_error('password', "Incorrect Password")
                    return render(request, 'login.html', {'form': form})
            except CustomUser.DoesNotExist:
                form.add_error('username', 'Username not found')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
