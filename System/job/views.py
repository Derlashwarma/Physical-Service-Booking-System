from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .forms import JobPostForm
from .models import Job, JobApplication
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

class JobViews:
    @login_required(login_url="login:login")
    def add_job(request):
        user = request.user
        if user.is_worker:
                return redirect('employee:employee_feed')
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
        job = get_object_or_404(Job, id=job_id)
        user = request.user

        job_application_exists = JobApplication.objects.filter(job=job, worker=user).exists()

        if request.method == 'POST':
            if job.employer == user:
                return HttpResponse("You cannot apply to your own job.")
            if job.is_done:
                return HttpResponse("Cannot apply to a completed job.")
            if job_application_exists:
                return HttpResponse("You have already applied for this job.")

            JobApplication.objects.create(job=job, worker=user)
            return redirect("job:apply_job", job_id=job_id)

        context = {
            'job': job,
            'user': user,
        }
        return render(request, 'apply_job.html', context)
    
    @login_required(login_url="login:login")
    def show_applications(request, job_id):
        if request.user.is_worker:
            return redirect("employee:employee_feed")
        
        job = Job.objects.get(id=job_id) 
        if job.employer != request.user and not request.user.is_staff :
            return redirect("employer:employer_feed")
        applications = JobApplication.objects.filter(job=job)

        owner = request.user == job.employer
        context = {
            'job': job,
            'applications': applications,
            'owner': owner
        }
        return render(request, 'job_detail.html',context)
    
    def accept_application(request, application_id):
        if request.method == 'POST':
            application = JobApplication.objects.get(pk=application_id)
            application.status = "accepted"
            application.save()

            return redirect("job:my_jobs", job_id=application.job.id)
        
    def reject_application(request, application_id):
        if request.method == 'POST':
            application = JobApplication.objects.get(pk=application_id)
            application.status = "declined"
            application.save()

            return redirect("job:my_jobs", job_id=application.job.id)
        
    def edit_job(request, job_id):
        job = Job.objects.get(pk=job_id)
        if request.user != job.employer and not request.user.is_staff:
            return HttpResponse("You Do Not Have Access")
        
        if request.method == 'POST':
            form = JobPostForm(request.POST, instance=job)
            if form.is_valid():
                form.save()
                return redirect("job:my_jobs", job_id=job.id)
        else:
            form = JobPostForm(instance=job)
        context = {
            'form': form,
            'job': job
        }
        return render(request, 'edit_job.html', context)
    
    def delete_job(request, job_id):
        job = Job.objects.get(pk=job_id)
        if request.method == 'POST':
            job.is_active = False
            job.save()
            return redirect('profile:profile',username=request.user.username)
        
        return render(request, 'delete_confirmation.html', {'job': job})

