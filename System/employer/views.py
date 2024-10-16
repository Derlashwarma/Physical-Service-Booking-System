from django.shortcuts import render

# Create your views here.
def employer_feed(request):
    return render(request, 'employer_feed.html')