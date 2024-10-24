from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .forms import JobPostForm
from .models import Job, JobApplication
from django.contrib.auth.decorators import login_required

class JobViews:
    @login_required(login_url="login:login")
    def add_job(request):
        user = request.user
        if request.method == 'POST':
            form = JobPostForm(request.POST)
            if form.is_valid():
                job = form.save(commit=False)
                job.employer = user
                job.save()
                return redirect('employer:employer_feed')
        else:
            form = JobPostForm()
        context = {
            'user': user,
            'form': form
        }
        return render(request, 'add_job.html',context)
    
    @login_required(login_url="login:login")
    def apply_job(request, job_id):
        job = Job.objects.get(id=job_id)
        try:
            jobApplication = JobApplication.objects.filter(job=job, worker=request.user).first()
        except JobApplication.DoesNotExist:
            jobApplication = None

        user = request.user
        if request.method == 'POST':
            if job.employer == user:
                return HttpResponse("Cannot Apply")
            elif jobApplication:
                return HttpResponse('Already Applied')
            application = JobApplication.objects.create(
                job = job,
                worker = user
            )
            application.save()
            return redirect("employee:employee_feed") 
        context = {
            'job': job,
            'user': user
        }
        return render(request, 'apply_job.html', context)