from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Min, Max, Sum
from django.utils import timezone
from datetime import timedelta
from register.models import CustomUser
from job.models import Job
from django.db.models import Q, Count

# Create your views here.
class AdminViews:
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
            return HttpResponse("You do not have access to this page")
        
        number_of_users = CustomUser.objects.count()
        number_of_jobs = Job.objects.count()
        finished_jobs = Job.objects.filter(is_done=True)
        income_generated = finished_jobs.aggregate(total_income=Sum('budget'))['total_income'] or 0

        date_started = timezone.datetime(2024, 10, 1)
        current_date = timezone.now()

        #List of registered users in a specific day
        daily_user_registration = AdminViews.get_daily_aggregates(
            model=CustomUser,
            date_field='date_joined',
            filter_kwargs={'date_joined__range': (date_started, current_date)},
            aggregation_field='id',
            aggregate_type=Count,
            order_by='date'
        )
        # dates = X, count = Y
        dates = [entry['date'] for entry in daily_user_registration]
        counts = [entry['aggregate_result'] for entry in daily_user_registration]

        # List of jobs created within the date range
        daily_jobs_created = AdminViews.get_daily_aggregates(
            model=Job,
            date_field='created_at',
            filter_kwargs={'created_at__range': (date_started, current_date)},
            aggregation_field='id',
            aggregate_type=Count,
            order_by='date'
        )
        
        # Dates and counts of jobs created
        job_dates = [entry['date'] for entry in daily_jobs_created]
        job_counts = [entry['aggregate_result'] for entry in daily_jobs_created]

         # Calculate daily income generated
        daily_income_generated = AdminViews.get_daily_aggregates(
            model=Job,
            date_field='finished_at',
            filter_kwargs={'finished_at__range':(date_started, current_date)},
            aggregation_field='budget',
            aggregate_type=Sum,
            order_by='date'
        )

        # Dates and daily income generated
        income_dates = [entry['date'] for entry in daily_income_generated]
        income_counts = [float(entry['aggregate_result']) for entry in daily_income_generated]
        print(income_counts)

        context = {
            'admin': user,
            'user_count': number_of_users,
            'job_count_sum': number_of_jobs,
            'income_generated': income_generated,
            'dates': dates,
            'count': counts,
            'job_date':job_dates,
            'job_count': job_counts,
            'income_date': income_dates,
            'income_count': income_counts
        }
        return render(request,'overview.html',context)
    
    
    @login_required(login_url="login:login")
    def user_admin_view(request):
        user = request.user
        if not user.is_superuser:
            return HttpResponse("You do not have access to this page")
        
        total_registered_users = CustomUser.objects.all().count()
        
        one_month_before = timezone.now() - timedelta(days=30)
        active_users = CustomUser.objects.filter(last_login__gte = one_month_before).count()

        worker_count = CustomUser.objects.filter(is_worker=True).count()
        employer_count = total_registered_users - worker_count

        date_started = timezone.datetime(2024, 10, 1)
        current_date = timezone.now()

        daily_user_registration = AdminViews.get_daily_aggregates(
            model=CustomUser,
            date_field='date_joined',
            filter_kwargs={'date_joined__range': (date_started, current_date)},
            aggregation_field='id',
            aggregate_type=Count,
            order_by='date'
        )
        # dates = X, count = Y
        dates = [entry['date'] for entry in daily_user_registration]
        counts = [entry['aggregate_result'] for entry in daily_user_registration]
        
        users = (
            CustomUser.objects
            .annotate(
                jobs_applied_count=Count('jobapplication'),
                jobs_created_count=Count('job'),
                accepted_jobs_count=Count('jobapplication', filter=Q(jobapplication__status='accepted')),
            )
            .values('username', 'is_worker', 'date_joined', 'jobs_applied_count', 'jobs_created_count', 'accepted_jobs_count')
        )
        context = {
            'total_users': total_registered_users,
            'active_users_count': active_users,
            'worker_count': worker_count,
            'employer_count': employer_count,
            'dates': dates,
            'counts': counts,
            'users': users,
        }
        
        return render(request, 'user_admin.html', context)