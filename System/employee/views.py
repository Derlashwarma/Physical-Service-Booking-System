from django.shortcuts import render

# Create your views here.
def employee_feed(request):
    return render(request, 'employee_feed.html')
