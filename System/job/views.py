from django.shortcuts import render, HttpResponse, redirect
from .forms import JobPostForm

# Create your views here.
def add_job(request):
    user = request.user
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = user
            job.save()
            return redirect('employer_feed')
    else:
        form = JobPostForm()
    context = {
        'user': user,
        'form': form
    }
    return render(request, 'add_job.html',context)