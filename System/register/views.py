from django.shortcuts import render, redirect, HttpResponse
from .forms import RegistrationForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            
            form.save()
            return HttpResponse("RETURN TO LOGIN REGISTRATION IS A SUCCESS")
    else:
        form = RegistrationForm()

    return render(request,'register.html', {'form':form})