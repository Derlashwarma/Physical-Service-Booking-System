from django.shortcuts import render
from job.models import Job


# Create your views here.
def employer_feed(request):
    jobs = Job.objects.filter(is_done=False)  
    context = {
        'jobs': jobs,
    }
    return render(request, 'employer_feed.html', context)