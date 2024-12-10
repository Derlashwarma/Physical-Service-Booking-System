from django.shortcuts import render
from job.models import Job, JobApplication
from rate.models import Rating
# Create your views here.
def employee_feed(request):
    jobs = Job.objects.filter(is_done=False, is_active=True)
    owner = request.user
    jobs_applied = JobApplication.objects.filter(worker=owner)

    selected_categories = request.GET.getlist('category')
    selected_schedules = request.GET.getlist('schedule')

    if selected_categories:
        jobs = jobs.filter(category__in=selected_categories)
    if selected_schedules:
        jobs = jobs.filter(schedule__in=selected_schedules)
    
    ratings = {
        'Timeliness': round(owner.get_average_rating('timeliness'),2),
        'Communication': round(owner.get_average_rating('communication'),2),
        'Professionalism': round(owner.get_average_rating('professionalism'),2)
    }
    context = {
        'jobs': jobs,
        'ratings': ratings,
        'owner': owner,
        'jobs_applied': jobs_applied,
        'CATEGORY_CHOICES': Job.CATEGORY_CHOICES,  
        'SCHEDULE_CHOICES': Job.SCHEDULE_CHOICES, 
    }
    return render(request, 'employee_feed.html', context)
