from django.shortcuts import render,redirect
from .models import Crisis
from django.contrib import messages
from management.models import Organization
import requests

def report(request):
    if request.method=="POST":
        print("POST data:", request.POST)
        if Crisis.objects.filter(name=request.POST['name'], description=request.POST['description']).exists():
            messages.error(request, 'This report has already been recorded.')
            return redirect('home')

        ip = requests.get('https://api64.ipify.org?format=json').json()['ip'] # Get the IP address of the user
        data = requests.get(f"https://geo.ipify.org/api/v2/country,city?apiKey=at_MzoWBhmT6WTpwaXGJ1E5k5t8FXLSM&ipAddress={ip}").json()
        
        crisis = Crisis(
            name=request.POST['name'],
            description=request.POST['description'],
            severitylvl=request.POST['severity'],
            currentstatus='R',
            lat=data['location']['lat'],
            lon=data['location']['lng'],
        )
        crisis.save()
        return redirect('incidents')

    return render(request, 'home.html')

def dashboard(request):
    if request.user.is_authenticated and (Organization.objects.filter(user=request.user).exists()):
        reports = Crisis.objects.exclude(assignee=request.user.organization, status='I').order_by('-time')
        mycrisis= Crisis.objects.filter(assignee=request.user.organization, status='I')
        if mycrisis:
            mycrisis = mycrisis[0]
            return render(request, 'incidents.html', {'mycrisis':mycrisis, 'crisis':reports})
    reports = Crisis.objects.order_by('-time')
    return render(request, 'incidents.html', {'crisis':reports})

# Create your views here.
