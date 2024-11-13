from django.shortcuts import render,redirect
from .models import Crisis
from django.contrib import messages

def report(request):
    if request.method=="POST":
        print("POST data:", request.POST)
        if Crisis.objects.filter(name=request.POST['name'], description=request.POST['description']).exists():
            messages.error(request, 'This report has already been recorded.')
            return redirect('report')

        crisis = Crisis(
            name=request.POST['name'],
            description=request.POST['description'],
            severitylvl=request.POST['severity'],
            currentstatus='R'
        )
        crisis.save()
        return redirect('dashboard')

    return render(request, 'home.html')

# Create your views here.
