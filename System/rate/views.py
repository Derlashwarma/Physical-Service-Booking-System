from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from register.models import CustomUser
from job.models import JobApplication
from .models import Rating, Review

@login_required(login_url='login:login')
def rate_user(request, username, job_id):
    user = get_object_or_404(CustomUser, username=username)

    if user.is_worker:
        application = get_object_or_404(JobApplication, job__id=job_id,worker=user)
        return __rate_worker(request, application)

    return HttpResponse("User is not a worker.")

def __rate_worker(request, application):
    timeliness_rating = request.POST.get('timeliness_rating', None)
    professionalism_rating = request.POST.get('professionalism_rating', None)
    communication_rating = request.POST.get('communication_rating', None)
    review = request.POST.get('review', "")

    if request.method == 'POST':

        if not timeliness_rating or not professionalism_rating or not communication_rating or not review:
            context = {
                'user': application.worker,
                'work': application.job,
                'employer': application.job.employer,
                'timeliness_rating': timeliness_rating,
                'professionalism_rating': professionalism_rating,
                'communication_rating': communication_rating,
                'review': review,
                'error': True
            }
            return render(request, 'rate_user.html', context)
        else:
            Rating.objects.create(name="timeliness",from_user=request.user,to_user=application.worker,score=timeliness_rating)
            Rating.objects.create(name="professionalism",from_user=request.user,to_user=application.worker,score=professionalism_rating)
            Rating.objects.create(name="communication",from_user=request.user,to_user=application.worker,score=communication_rating)
            Review.objects.create(from_user=request.user,to_user=application.worker,review=review)
            application.rated = True
            application.save()
            return redirect('job:my_jobs', application.job.id)

    context = {
        'user': application.worker,
        'work': application.job,
        'employer': application.job.employer
    }
    return render(request, 'rate_user.html', context)

def __rate_employer(request, username):
    # Placeholder for employer rating (can be implemented similarly)
    pass
