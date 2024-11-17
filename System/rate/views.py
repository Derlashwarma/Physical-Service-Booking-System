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
        user = get_object_or_404(CustomUser , username=username)
    except Http404:
        return HttpResponse("User is not found", status=404)

    if user.is_worker:
        return handle_worker_rating(request, user, job_id)
    else:
        return handle_employer_rating(request, user, job_id)

def handle_worker_rating(request, worker, job_id):
    try:
        application = get_object_or_404(JobApplication, job__id=job_id, worker=worker)
    except Http404:
        return HttpResponse("Application not found", status=404)
    
    if application.rated:
        return HttpResponse("You already rated this user", status=404)
    
    if application.status not in ['completed']:
        return HttpResponse("Do not have access", status=404)

    return __rate_worker(request, application)

def __rate_worker(request, application):
    if request.method == 'POST':
        return process_worker_rating(request, application)

    return render_rating_form(request, application.worker, application.job)

def process_worker_rating(request, application):
    timeliness_rating = request.POST.get('timeliness_rating')
    professionalism_rating = request.POST.get('professionalism_rating')
    communication_rating = request.POST.get('communication_rating')
    review = request.POST.get('review', "")

    if not all([timeliness_rating, professionalism_rating, communication_rating, review]):
        return render_rating_form(request, application.worker, application.job, error=True)

    save_worker_rating(request.user, application.worker, timeliness_rating, professionalism_rating, communication_rating, review)
    application.rated = True
    application.save()
    
    return redirect('job:my_jobs', application.job.id)

def save_worker_rating(from_user, to_user, timeliness, professionalism, communication, review):
    Rating.objects.create(name="timeliness", from_user=from_user, to_user=to_user, score=timeliness)
    Rating.objects.create(name="professionalism", from_user=from_user, to_user=to_user, score=professionalism)
    Rating.objects.create(name="communication", from_user=from_user, to_user=to_user, score=communication)
    Review.objects.create(from_user=from_user, to_user=to_user, review=review)

    
def render_rating_form(request, user, job, error=False):
    context = {
        'user': user,
        'work': job,
        'employer': job.employer,
        'error': error
    }
    return render(request, 'rate_user.html', context)


def handle_employer_rating(request, user, job_id):
    try:
        job = get_object_or_404(Job, id=job_id)
        # application = get_object_or_404(JobApplication, job=job, worker=user, status='completed')
    except Http404:
        return HttpResponse("Not found", status=404)

    if job.rated:
        return HttpResponse("You already rated this employer", status=404)

    return __rate_employer(request, job)

def __rate_employer(request, job):
    if request.method == 'POST':
        return process_employer_rating(request, job)

    return render_employer_rating_form(request, job)

def process_employer_rating(request, job):
    communication_rating = request.POST.get('communication_rating')
    fairness_respect_rating = request.POST.get('fairness_respect_rating')
    timeliness_payment_rating = request.POST.get('timeliness_payment_rating')
    review = request.POST.get('review', "")

    if not all([communication_rating, fairness_respect_rating, timeliness_payment_rating, review]):
        return render_employer_rating_form(request, job, error=True)

    save_employer_rating(request.user, job.employer, communication_rating, fairness_respect_rating, timeliness_payment_rating, review)
    job.rated = True
    job.save()

    return redirect('job:apply_job', job.id)

def save_employer_rating(from_user, to_user, communication, fairness, timeliness, review):
    Rating.objects.create(name="communication", from_user=from_user, to_user=to_user, score=communication)
    Rating.objects.create(name="fairness_respect", from_user=from_user, to_user=to_user, score=fairness)
    Rating.objects.create(name="timeliness_payment", from_user=from_user, to_user=to_user, score=timeliness)
    Review.objects.create(from_user=from_user, to_user=to_user, review=review)

def render_employer_rating_form(request, job, error=False):
    context = {
        'employer': job.employer,
        'work': job,
        'error': error
    }
    return render(request,'rate_employer.html',context)