from django.shortcuts import render
from job.models import Job, JobApplication
from rate.models import Rating

# Create your views here.
def employer_feed(request):
    owner = request.user
    if request.user.is_authenticated:
        jobs_posted_by_user = Job.objects.filter(employer=owner)
        applications = JobApplication.objects.filter(job__in=jobs_posted_by_user)
        active_jobs = jobs_posted_by_user.filter(is_done=False, is_active=True)
        ratings = {
            'Fairness_Respect': round(owner.get_average_rating('fairness_respect'), 2),
            'Communication': round(owner.get_average_rating('communication'), 2),
            'Timeliness_Payment': round(owner.get_average_rating('timeliness_payment'), 2),
        }
    else:
        applications = None
        active_jobs = None
        ratings = None

    context = {
        'active_jobs': active_jobs,
        'ratings': ratings,
        'applications': applications,
        'owner': owner,
    }
    return render(request, 'employer_feed.html', context)
