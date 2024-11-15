from django.shortcuts import render,redirect
from .models import Crisis
from django.contrib import messages
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
        return redirect('dashboard')

    return render(request, 'home.html')

# Create your views here.
