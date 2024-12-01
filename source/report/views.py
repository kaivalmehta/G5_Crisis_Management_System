from django.shortcuts import render,redirect
from .models import Crisis
from django.contrib import messages
from management.models import Organization
import requests
import json

def report(request):
    if request.method=="POST":
        print("POST data:", request.POST)
        if Crisis.objects.filter(name=request.POST['name'], description=request.POST['description']).exists():
            messages.error(request, 'This report has already been recorded.')
            return redirect('home')

        # ip = requests.get('https://api64.ipify.org?format=json').json()['ip'] # Get the IP address of the user
        # data = requests.get(f"https://geo.ipify.org/api/v2/country,city?apiKey=at_MzoWBhmT6WTpwaXGJ1E5k5t8FXLSM&ipAddress={ip}").json()
        lat=request.POST.get("latitude")
        lon=request.POST.get("longitude")

        crisis = Crisis(
            name=request.POST['name'],
            description=request.POST['description'],
            severitylvl=request.POST['severity'],
            currentstatus='R',
            lat=lat,
            lon=lon
        )
        crisis.save()
        return redirect('incidents')

    return render(request, 'home.html')

def dashboard(request):
    if request.user.is_authenticated and (Organization.objects.filter(user=request.user).exists()):
        reports = Crisis.objects.exclude(assignee=request.user.organization, currentstatus='I').order_by('-time')
        mycrisis= Crisis.objects.filter(assignee=request.user.organization, currentstatus='I')
        if mycrisis.exists():
            return render(request, 'incidents.html', {'mycrisis':mycrisis, 'crisis':reports})
    reports = Crisis.objects.order_by('-time')
    return render(request, 'incidents.html', {'crisis':reports})

def respond(request,cID):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in first.")
        return redirect('login')
    report = Crisis.objects.filter(crisisID=cID)
    if report:
        report = report[0]
    else:
        messages.error(request, "Some Error Occured.")
        return redirect('incidents')
    
    if report.assignee is not None:
        messages.error(request, "Task already assigned.")
        return redirect('incidents')

    report.assignee = request.user.organization
    report.currentstatus = 'I'
    request.user.organization.save()
    report.save()
    return redirect('incidents')

def solve(request, cID):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in first.")
        return redirect('login')
    report = Crisis.objects.filter(crisisID=cID)
    if report:
        report = report[0]
    
  
    report.currentstatus = 'S'
    request.user.organization.save()
    report.assignee=None
    report.save()
    return redirect('incidents')
