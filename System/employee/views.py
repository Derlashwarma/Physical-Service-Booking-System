from django.shortcuts import render
from job.models import Job
# Create your views here.
def employee_feed(request):
    jobs = Job.objects.filter(is_done=False)
    context = {
        'jobs': jobs,
    }
    return render(request, 'employee_feed.html', context)
