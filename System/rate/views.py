from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from register.models import CustomUser
from job.models import JobApplication, Job
from .models import Rating, Review
from django.http import Http404

@login_required(login_url='login:login')
def rate_user(request, username, job_id):
    try:
        user = get_object_or_404(CustomUser, username=username)
    except Http404:
        return HttpResponse("Do not have access")

    if user.is_worker:
        try:
            application = get_object_or_404(JobApplication, job__id=job_id,worker=user)
        except Http404:
            return HttpResponse("Do not have access")
        if application.rated or application.status not in ['completed', 'completed']:
            return HttpResponse("do not have access")
        return __rate_worker(request, application)
    
    else:
        try:
            job = get_object_or_404(Job, id=job_id)
            user = CustomUser.objects.get(pk=request.user.id)
            application = get_object_or_404(JobApplication, job=job, worker=user, status='completed')
            return __rate_employer(request, job)
        except CustomUser.DoesNotExist:
            return HttpResponse("USer not found")
        except Http404:
            return HttpResponse("Do not have access")

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

def __rate_employer(request, job):
    communication_rating = request.POST.get('communication_rating', None)
    fairness_respect_rating = request.POST.get('fairness_respect_rating', None)
    timeliness_payment_rating = request.POST.get('timeliness_payment_rating', None)
    review = request.POST.get('review', "")
    
    if request.method == 'POST':
        if not fairness_respect_rating or not timeliness_payment_rating or not communication_rating or not review:
            context = {
                'employer': job.employer,
                'work': job,
            }
            return render(request, 'rate_user.html', context)
        else:
            Rating.objects.create(name="communication",from_user=request.user,to_user=job.employer,score=communication_rating)
            Rating.objects.create(name="fairness_respect",from_user=request.user,to_user=job.employer,score=fairness_respect_rating)
            Rating.objects.create(name="timeliness_payment",from_user=request.user,to_user=job.employer,score=timeliness_payment_rating)
            Review.objects.create(from_user=request.user,to_user=job.employer,review=review)
            job.rated = True
            job.save()
            return redirect('profile:profile', request.user.username)

    context = {
        'employer': job.employer,
        'work': job,
    }
    return render(request,'rate_employer.html',context)
