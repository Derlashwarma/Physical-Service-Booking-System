from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Min, Max, Sum
from django.utils import timezone
from register.models import CustomUser
from job.models import Job

# Create your views here.
class AdminViews:
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
        daily_user_registration = (
            CustomUser.objects.filter(date_joined__range=(date_started, current_date))
            .extra({'date': 'date(date_joined)'})
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date')
        )
        # dates = X, count = Y
        dates = [entry['date'] for entry in daily_user_registration]
        counts = [entry['count'] for entry in daily_user_registration]

        # List of jobs created within the date range
        daily_jobs_created = (
            Job.objects.filter(created_at__range=(date_started, current_date))
            .extra({'date': 'date(created_at)'})
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date')
        )
        
        # Dates and counts of jobs created
        job_dates = [entry['date'] for entry in daily_jobs_created]
        job_counts = [entry['count'] for entry in daily_jobs_created]

         # Calculate daily income generated
        daily_income_generated = (
            Job.objects.filter(is_done=True, finished_at__range=(date_started, current_date))
            .extra({'date': 'date(finished_at)'}) 
            .values('date')
            .annotate(daily_income=Sum('budget')) 
            .order_by('date')
        )

        # Dates and daily income generated
        income_dates = [entry['date'] for entry in daily_income_generated]
        income_counts = [float(entry['daily_income']) for entry in daily_income_generated]
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