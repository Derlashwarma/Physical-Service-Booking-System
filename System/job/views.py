from django.shortcuts import render, redirect, get_object_or_404
from .forms import JobPostForm
from .models import Job, JobApplication
from django.contrib.auth.decorators import login_required
from django.contrib import messages

class JobViews:
    @login_required(login_url="login:login")
    def add_job(request):
        user = request.user
        if user.is_worker:
                return render(request, 'access_errors.html', {
                     'status': 405,
                     'message': 'Method Access Forbidden' 
                })
        if request.method == 'POST':
            form = JobPostForm(request.POST)
            if form.is_valid():
                job = form.save(commit=False)
                job.employer = user
                job.save()
                messages.add_message(request,messages.SUCCESS,'Job Added Successfully')
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
        try:
            job = get_object_or_404(Job, id=job_id)
            user = request.user

            job_application_exists = JobApplication.objects.filter(job=job, worker=user).exists()

            if request.method == 'POST':
                if job.employer == user:
                    return render(request,'access_errors.html',
                                {
                                    'status': 403,
                                    'message': 'Action forbidden, you cannot access this operation'
                                })
                if job.is_done:
                    return render(request,'access_errors.html',
                                {
                                    'status': 403,
                                    'message': 'Action forbidden, you have already rated this job.'
                                })

                JobApplication.objects.create(job=job, worker=user)
                messages.add_message(request,messages.SUCCESS,'Application Sent Successfully')
                return redirect("job:apply_job", job_id=job_id)
            if job_application_exists:
                context = {
                    'job': job,
                    'user': user,
                    'applied': job_application_exists,
                'category': ((job.category).replace('_',' '))
                }
                return render(request, 'apply_job.html', context)
            context = {
                'job': job,
                'user': user,
                'category': ((job.category).replace('_',' '))
            }
            return render(request, 'apply_job.html', context)
        except Job.DoesNotExist:
                    return render(request,'access_errors.html',
                                {
                                    'status': 404,
                                    'message': 'Job Not Found'
                                })
        except Exception as e:
            return render(request, 'access_errors.html', {
                'status': 500,
                'message': 'An unexpected error occurred: {}'.format(str(e)),
            })
        
    @login_required(login_url="login:login")
    def show_applications(request, job_id):
        try:
            if request.user.is_worker:
                return render(request, 'access_errors.html', {
                     'status': 405,
                     'message': 'Access Forbidden'
                }) 
            
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
        except Job.DoesNotExist:
                return render(request,'access_errors.html',
                              {
                                  'status': 404,
                                  'message': 'Job does not exist'
                              })
        except Exception as e:
            return render(request, 'access_errors.html', {
                'status': 500,
                'message': 'An unexpected error occurred: {}'.format(str(e)),
            })
            
    
    def accept_application(request, application_id):
        if request.method == 'POST':
            try:
                    application = JobApplication.objects.get(pk=application_id)
                    application.status = "accepted"
                    application.save()
                    messages.add_message(request,messages.SUCCESS,'Application was Accepted Successfully')
                    return redirect("job:my_jobs", job_id=application.job.id)
            except JobApplication.DoesNotExist:
                    return render(request,'access_errors.html',
                                {
                                    'status': 404,
                                    'message': 'Job Application Not Found'
                                })
        else:
            return render(request, 'access_errors.html', {
                'status': 405,
                'message': 'Method Access Forbidden'
            }, status=405)


    def reject_application(request, application_id):
        if request.method == 'POST':
            try:
                application = JobApplication.objects.get(pk=application_id)
                if request.user != application.job.employer:
                     return render(request, "access_errors.html",
                      {
                           'status': 405,
                           'message': 'Action is not allowed'
                      })
                    
                application.status = "declined"
                application.save()
                messages.add_message(request,messages.SUCCESS,'Application was Declined Successfully')
                return redirect("job:my_jobs", job_id=application.job.id)
            except JobApplication.DoesNotExist:
                return render(request, 'access_errors.html', {
                    'status': 404,
                    'message': 'Job Application Not Found',
                })
        return render(request, 'access_errors.html', {
            'status': 405,
            'message': 'Method Access Forbidden',
        }, status=405)
        

    def edit_job(request, job_id):
        try:
            job = Job.objects.get(pk=job_id)
            if request.user != job.employer and not request.user.is_staff:
                return render(request, 'access_errors.html', {
                     'status': 405,
                     'message': 'Access Forbidden'
                })
            
            if request.method == 'POST':
                form = JobPostForm(request.POST, instance=job)
                if form.is_valid():
                    form.save()
                    messages.add_message(request,messages.SUCCESS,'Job Was Successfully Changed')
                    return redirect("job:my_jobs", job_id=job.id)
            else:
                form = JobPostForm(instance=job)
            context = {
                'form': form,
                'job': job
            }
            return render(request, 'edit_job.html', context)
        except Job.DoesNotExist:
                    return render(request,'access_errors.html',
                                {
                                    'status': 404,
                                    'message': 'Job Not Found'
                                })
        except Exception as e:
            return render(request, 'access_errors.html', {
                'status': 500,
                'message': 'An unexpected error occurred: {}'.format(str(e)),
            })
        

    def delete_job(request, job_id):
        try:
            job = Job.objects.get(pk=job_id)
            if request.method == 'POST':
                job.is_active = False
                job.save()
                messages.add_message(request,messages.SUCCESS,'Job was Deleted Successfully')
                return redirect('profile:profile', username=request.user.username)
        except Job.DoesNotExist:
            return render(request, 'access_errors.html', {
                'status': 404,
                'message': 'Job Not Found'
            })
        except Exception as e:
            return render(request, 'access_errors.html', {
                'status': 500,
                'message': 'An unexpected error occurred: {}'.format(str(e)),
            })
        return render(request, 'delete_confirmation.html', {'job': job})