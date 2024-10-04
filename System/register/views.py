from django.shortcuts import render, redirect, HttpResponse
from .forms import RegistrationForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['is_worker'] = form.cleaned_data.get('is_worker')
            return redirect('register:register_success')
        else:
            password_error = form.errors.get('password')
            username_error = form.errors.get('username')
            is_worker_error = form.errors.get('is_worker')

            return render(request,'register.html', {'form':form, 'password_error':password_error, 'username_error':username_error, 'is_worker_error': is_worker_error})
    else:
        form = RegistrationForm()

    return render(request,'register.html', {'form':form})

def register_success(request):
    is_worker = request.session.get('is_worker', False)
    if is_worker == "True":
        string = "You’re now part of a vibrant community where you can connect with local professionals and find opportunities."
    else:
        string = "Congratulations! Your account is successfully created. You’re now ready to explore and hire top talents tailored to your needs. "
    return render(request, 'register_success.html', {'string':string})