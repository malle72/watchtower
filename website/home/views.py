from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
    content = {'about':"A little blurb about the purpose of this website."}
    return render(request, 'home/home.html', content)

def trackers(request):
    # TODO will need to pull list of all tracker apps
    return render(request, 'home/trackers.html')

def reports(request):
    # TODO will need to pull list of all reports
    return render(request, 'home/reports.html')