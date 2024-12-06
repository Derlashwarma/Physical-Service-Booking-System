from django.shortcuts import render, HttpResponse, redirect
from register.models import CustomUser
from rate.models import Rating, Review
from .forms import UserProfileForm
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.contrib.auth.decorators import login_required
from job.models import JobApplication
from job.models import Job
from django.db.models import Q
from django.contrib import messages

@login_required(login_url="login:login")
def profile(request, username):
    try:
        user = CustomUser.objects.get(username=username)
        logged_in_user = request.user
        user_id = request.user.id

        owner = user == request.user

        if user_id is None:
            return redirect('login:login')
        
        if request.user.is_worker:
            mutual_connection_exists = JobApplication.objects.filter(Q(worker=logged_in_user, job__employer=user)).exists() | owner
        elif not request.user.is_worker:
            mutual_connection_exists = JobApplication.objects.filter(Q(worker=user, job__employer=logged_in_user)).exists() | owner
            
        if user.is_worker and mutual_connection_exists:
            return display_worker_profile(request, user, request.user, owner)
        elif not user.is_worker and mutual_connection_exists:
            return display_employer_profile(request, user, request.user, owner)
        else:
            return render(request, 'access_errors.html', {
                'status': 403,
                'message': 'Access Forbidden, You Do Not Have Connections'
            },status=403)
    except CustomUser.DoesNotExist:
        return render(request, 'access_errors.html', {
                'status': 404,
                'message': 'User Not Found'
            },status=404)
    except Exception as e:
        return render(request, 'access_errors.html', {
                'status': 403,
                'message': f'An Exception Occured: {e}'
        })
        
    

@login_required(login_url="login:login")
def display_worker_profile(request, user, logged_in_user, owner):
    professional_experience = user.professional_experience
    professional_summary = user.professional_summary
    key_skills = user.key_skills
    social_contacts = user.social_contacts
    profile_picture = user.image
    jobs_applied = JobApplication.objects.filter(worker=user)
    reviews = Review.objects.filter(to_user=user)
    ratings = {
        'Timeliness': round(user.get_average_rating('timeliness'),2),
        'Communication': round(user.get_average_rating('communication'),2),
        'Professionalism': round(user.get_average_rating('professionalism'),2)
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
        'ratings': ratings,
        'jobs': jobs_applied,
        'reviews':reviews
    }
    return render(request, 'profile.html', context)

#This function will render the template for the Employer's profile
@login_required(login_url="login:login")
def display_employer_profile(request, user, logged_in_user, owner):
    active_jobs = Job.objects.filter(employer= user, is_done=False, is_active=True)
    finished_jobs = Job.objects.filter(employer= user, is_done=True)
    reviews = Review.objects.filter(to_user=user)
    
    ratings = {
        'Fairness_Respect': round(user.get_average_rating('fairness_respect'),2),
        'Communication': round(user.get_average_rating('communication'),2),
        'Timeliness_Payment': round(user.get_average_rating('timeliness_payment'),2)
    }
    context = {
        'profile_owner': user,
        'user': logged_in_user,
        'active_jobs': active_jobs,
        'ratings': ratings,
        'finished_jobs': finished_jobs,
        'owner': owner,
        'reviews': reviews
    }
    return render(request, 'employer_profile.html', context)

@login_required(login_url="login:login")
def edit_profile(request,username):
    try:
        user = CustomUser.objects.get(username=username)
        if user != request.user:
            return render(request, 'access_errors.html', {
                'status': 403,
                'message': 'Access Forbidden'
            }, status=403)

        if request.method == "POST":
            form = UserProfileForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                messages.add_message(request,messages.SUCCESS,'Changes was Successfuly saved')
                return redirect('profile:profile', username=username)
        else:
            form = UserProfileForm(instance=user)
        context = {
            'user': user,
            'form': form
        }
        return render(request, 'edit_profile.html', context)
    except CustomUser.DoesNotExist:
        return render(request, 'access_errors.html', {
            'status': 404,
            'message': 'User Not Found'
        }, status=404)
    except Exception as e:
        return render(request, 'access_errors.html', {
            'status': 405,
            'message': f'Something wrong happend: {e}'
        }, status=405)
