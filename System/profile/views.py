from django.shortcuts import render, HttpResponse, redirect
from register.models import CustomUser
from .forms import UserProfileForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

#This function will accept username as a parameter and render the profile of the username
@login_required(login_url="login:login")
def profile(request, username):
    user = CustomUser.objects.get(username=username)
    user_id = request.user.id
    logged_in_user = CustomUser.objects.get(id=user_id)

    owner = user == logged_in_user
    if user_id is None:
        return redirect('login:login')

    #If worker render the template profile.html and pass necessary values
    if user.is_worker:
        return display_worker_profile(request, user, logged_in_user, owner)
    else:
        return HttpResponse('not a worker')
    
#This function will render the template and pass the requirements
@login_required(login_url="login:login")
def display_worker_profile(request, user, logged_in_user,owner):
    professional_experience = user.professional_experience
    professional_summary = user.professional_summary
    key_skills = user.key_skills
    social_contacts = user.social_contacts
    profile_picture = user.image
    ratings = {
        'Timeliness': user.get_average_rating('timeliness'),
        'Communication': user.get_average_rating('communication'),
        'Professionalism': user.get_average_rating('professionalism')
    }
    context = {
        'owner': owner,
        'logged_in_user': logged_in_user ,
        'username': user.username,
        'experience': professional_experience,
        'summary': professional_summary,
        'skills': key_skills,
        'social': social_contacts,
        'profile': profile_picture,
        'ratings': ratings
    }
    return render(request, 'profile.html', context)

#This function will render the template for the Employer's profile
@login_required(login_url="login:login")
def display_employer_profile():
    pass

@login_required(login_url="login:login")
def edit_profile(request,username):
    user = request.user
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile:profile', username=username)
    else:
        form = UserProfileForm(instance=user)
    context = {
        'user': user,
        'form': form
    }
    return render(request, 'edit_profile.html', context)