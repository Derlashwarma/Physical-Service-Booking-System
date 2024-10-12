from django.shortcuts import render, HttpResponse, redirect
from register.models import User
from .forms import UserProfileForm
from django.shortcuts import render, get_object_or_404, redirect

#This function will accept username as a parameter and render the profile of the username 
def profile(request, username):
    user = User.objects.get(username=username)
    user_id = request.session.get('id')
    logged_in_user = User.objects.get(id=user_id)

    owner = user == logged_in_user
    if user_id is None:
        return redirect('login:login')

    #If worker render the template profile.html and pass necessary values
    if user.is_worker:
        return display_worker_profile(request, user, logged_in_user, owner)
    else:
        return HttpResponse('not a worker')
    
#This function will render the template and pass the requirements
def display_worker_profile(request, user, logged_in_user,owner):
    professional_experience = user.professional_experience
    professional_summary = user.professional_summary
    key_skills = user.key_skills
    social_contacts = user.social_contacts
    ratings = user.ratings.all()
    profile_picture = user.image
    context = {
        'owner': owner,
        'logged_in_user': logged_in_user ,
        'username': user.username,
        'experience': professional_experience,
        'summary': professional_summary,
        'skills': key_skills,
        'social': social_contacts,
        'ratings': ratings,
        'profile': profile_picture,
    }
    return render(request, 'profile.html', context)

#This function will render the template for the Employer's profile
def display_employer_profile():
    pass

def edit_profile(request,username):
    user = get_object_or_404(User, username=username)
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