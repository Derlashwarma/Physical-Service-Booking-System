from django.shortcuts import render, redirect, HttpResponse
from .forms import RegistrationForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data['password']
            password2 = request.POST.get('confirm_password')
            if password1 != password2:
                form.add_error("password", 'Passwords do not match')
                return render(request,'register.html', {'form':form})

            form.save()
            request.session['is_worker'] = form.cleaned_data.get('is_worker')
            return redirect('register:register_success')
        else:
            return render(request,'register.html', {'form':form})
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