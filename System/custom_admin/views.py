from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Min, Max, Sum
from django.utils import timezone
from datetime import timedelta
from register.models import CustomUser
from job.models import Job, JobApplication
from django.db.models import Q, Count
from register.forms import AdminUserForm
from .forms import ApplicationForm
from collections import Counter
from django.core.cache import cache
from django.utils.decorators import method_decorator

# Create your views here.
class AdminViews:
    @staticmethod
    def get_daily_aggregates(model, date_field, filter_kwargs, aggregation_field='id',
                              aggregate_type=Count, order_by='date'):
        return (
            model.objects.filter(**filter_kwargs)
            .extra({'date': f'date({date_field})'})
            .values('date')
            .annotate(aggregate_result=aggregate_type(aggregation_field))
            .order_by(order_by)
        )
    
    @login_required(login_url="login:login")
    def overview(request):
        user = request.user
        if not user.is_superuser:
            return render(request, "access_errors.html", {'status':403})
        
        # Consolidate number of users and jobs into a single database hit
        aggregate_data = cache.get('overview_aggregate_data')
        if aggregate_data is None:
            aggregate_data = {
                'number_of_users': CustomUser.objects.count(),
                'number_of_jobs': Job.objects.count(),
                'total_income': Job.objects.filter(is_done=True).aggregate(total_income=Sum('budget'))['total_income'] or 0,
            }

            #change if ideploy but its highly unllikely
            cache.set('overview_aggregate_date',aggregate_data, 500)

        date_started = timezone.datetime(2024, 10, 1)
        current_date = timezone.now()


        daily_user_registration = cache.get("daily_user_registration")
        if daily_user_registration is None:
            daily_user_registration = AdminViews.get_daily_aggregates(
                model=CustomUser,
                date_field='date_joined',
                filter_kwargs={'date_joined__range': (date_started, current_date)},
                aggregation_field='id',
                aggregate_type=Count,
                order_by='date'
            )
            cache.set('daily_user_registration', daily_user_registration)

        dates = [entry['date'] for entry in daily_user_registration]
        counts = [entry['aggregate_result'] for entry in daily_user_registration]

        daily_jobs_created = cache.get('daily_jobs_created')
        if daily_jobs_created is None:
            daily_jobs_created = AdminViews.get_daily_aggregates(
                model=Job,
                date_field='created_at',
                filter_kwargs={'created_at__range': (date_started, current_date)},
                aggregation_field='id',
                aggregate_type=Count,
                order_by='date'
            )
            cache.set('daily_jobs_created', daily_jobs_created)
        job_dates = [entry['date'] for entry in daily_jobs_created]
        job_counts = [entry['aggregate_result'] for entry in daily_jobs_created]

        daily_income_generated = cache.get('daily_income_generated')
        if daily_income_generated is None:
            daily_income_generated = AdminViews.get_daily_aggregates(
                model=Job,
                date_field='finished_at',
                filter_kwargs={'finished_at__range':(date_started, current_date)},
                aggregation_field='budget',
                aggregate_type=Sum,
                order_by='date'
            )
            cache.set('daily_income_generated', daily_income_generated)

        income_dates = [entry['date'] for entry in daily_income_generated]
        income_counts = [float(entry['aggregate_result']) for entry in daily_income_generated]

        context = {
            'admin': user,
            'user_count': aggregate_data['number_of_users'],
            'job_count_sum': aggregate_data['number_of_jobs'],
            'income_generated': aggregate_data['total_income'],
            'dates': dates,
            'count': counts,
            'job_date': job_dates,
            'job_count': job_counts,
            'income_date': income_dates,
            'income_count': income_counts
        }

        return render(request, 'overview.html', context)
    
    
    @login_required(login_url="login:login")
    def user_admin_view(request):
        user = request.user
        if not user.is_superuser:
            return render(request, "access_errors.html", {'status':403})
        
        user_counts = cache.get('user_count')
        if user_counts is None:
            user_counts = CustomUser.objects.aggregate(
                total_users=Count('id'),
                worker_count=Count('id', filter=Q(is_worker=True)),
                active_users=Count('id', filter=Q(last_login__gte=timezone.now() - timedelta(days=30))),
            )
            cache.set('user_count',user_counts)
        
        employer_count = user_counts['total_users'] - user_counts['worker_count']

        # Precompute daily user registration stats (consider caching)
        date_started = timezone.datetime(2024, 10, 1)
        current_date = timezone.now()
        
        daily_user_registration = cache.get('daily_user_registration')
        if daily_user_registration is None:
            return redirect('custom_admin:overview')
        
        dates = [entry['date'] for entry in daily_user_registration]
        counts = [entry['aggregate_result'] for entry in daily_user_registration]
        
        # Sorting options for user list
        current_sort_option = request.GET.get("sort_option", "date_joined")
        sort_by = request.GET.get("sort_by", "-")
        order_args = [f"{'-' if sort_by == '-' else ''}{current_sort_option}"]
        
        # Annotate with counts and order by specified field
        users = (
            CustomUser.objects
            .annotate(
                jobs_applied_count=Count('jobapplication'),
                jobs_created_count=Count('job'),
                accepted_jobs_count=Count('jobapplication', 
                                          filter=Q(jobapplication__status__in=['accepted','completed'])),
            )
            .values('id', 'username', 'is_worker', 'date_joined', 'jobs_applied_count', 'jobs_created_count', 'accepted_jobs_count')
            .order_by(*order_args)
        )
        
        context = {
            'total_users': user_counts['total_users'],
            'active_users_count': user_counts['active_users'],
            'worker_count': user_counts['worker_count'],
            'employer_count': employer_count,
            'dates': dates,
            'counts': counts,
            'users': users,
            'current_sort_option': current_sort_option,
            'sort_by': sort_by,
        }
        
        return render(request, 'user_admin.html', context)
    
    @login_required(login_url="login:login")
    def edit_user_admin_view(request, user_id):
        logged_user = request.user
        if not logged_user.is_superuser:
            return render(request, "access_errors.html", {'status':403})
        
        profile = CustomUser.objects.get(pk=user_id)
        if request.method == 'POST':
            form = AdminUserForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('custom_admin:users')
        else:
            form = AdminUserForm(instance=profile)
        context = {
            'form': form,
            'user': profile
        }
        return render(request, 'edit_users_admin.html', context)
    
    @login_required(login_url="login:login")
    def job_application_admin(request):
        logged_user = request.user
        if not logged_user.is_superuser:
            return render(request, "access_errors.html", {'status':403})
        
        applications_overview = cache.get('application_overview')
        if applications_overview is None:
            applications_overview = (
                JobApplication.objects.aggregate(
                    total_applications=Count('id'),
                    total_pending_applications=Count('id', filter=Q(status='pending')),
                    total_accepted_applications=Count('id', filter=Q(status='accepted')),
                    total_completed=Count('id', filter=Q(status='completed')),
                )
            )
            cache.set('application_overview',applications_overview)

        applications = JobApplication.objects.all()

        context = {
            'application_overview':applications_overview,
            'applications': applications,

        }
        return render(request,'job_application_admin.html', context)

    @login_required(login_url="login:login")
    def edit_application(request, application_id):
        logged_user = request.user
        if not logged_user.is_superuser:
            return render(request, "access_errors.html", {'status':403})
        
        application = JobApplication.objects.get(pk=application_id)
        if request.method == 'POST':
            form = ApplicationForm(request.POST,instance=application)
            if form.is_valid():
                form.save()
                return redirect('custom_admin:job_applications')
        else:
            form = ApplicationForm(instance=application)

        context = {
            'form': form
        }
        return render(request, 'edit_application.html',context)


    @login_required(login_url="login:login")
    def job_admin(request):
        logged_user = request.user
        if not logged_user.is_superuser:
            return render(request, "access_errors.html", {'status':403})
        
        job_summary = cache.get('job_summary')
        if job_summary is None:
            job_summary = {
                'job_posted': Job.objects.all().count(),
                'active': Job.objects.filter(is_done=False).count(),
                'completed': Job.objects.filter(is_done=True).count(),
                'revenue': Job.objects.filter(is_done=True).aggregate(Sum('budget'))['budget__sum']
            }
            cache.set('job_summary', job_summary)

        daily_jobs_created = cache.get('daily_jobs_created')
        if daily_jobs_created is None:
            return redirect("custom_admin:overview")
        job_dates = [entry['date'] for entry in daily_jobs_created]
        job_counts = [entry['aggregate_result'] for entry in daily_jobs_created]

        job_types = Job.objects.values_list('category', flat=True)
        job_tags = Counter(job_types)
        tag = {
            'label': list(job_tags.keys()),
            'count': list(job_tags.values())
        }

        current_sort_option = request.GET.get("sort_option", "title")
        sort_by = request.GET.get("sort_by", "-")
        order_args = [f"{'-' if sort_by == '-' else ''}{current_sort_option}"]
        
        jobs = Job.objects.order_by(*order_args)
        context = {
            'job_summary': job_summary,
            'job_date': job_dates,
            'job_count': job_counts,
            'tag': tag,
            'jobs': jobs,
            'current_sort_option': current_sort_option
        }
        return render(request, 'job_admin.html', context)
        