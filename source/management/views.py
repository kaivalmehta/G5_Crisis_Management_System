# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .forms import VolunteerForm,OrganizationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .forms import VolunteerForm, OrganizationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        if User.objects.filter(username=request.POST['email']).exists():
            messages.error(request, "E-mail already exists.")
            return redirect('register')

        if request.POST['password'] != request.POST['confpassword']:
            messages.error(request, "The passwords entered do not match.")
            return redirect('register')

        if len(request.POST['password']) < 8:
            messages.error(request, "Password length is too short.")
            return redirect('register')

        user = User(first_name=request.POST['name'], username=request.POST['email'])
        user.set_password(request.POST['password'])  # Hashes the password
        request.session['username'] = user.username
        user.save()
        if request.POST['type'] == "volunteer":
            return redirect('volregister')
        else:
            return redirect('orgregister')

    return render(request, 'register.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        user = authenticate(username=request.POST['email'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    return render(request, 'login.html')
def volregister(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = VolunteerForm()
    user = User.objects.get(username=request.session['username'])
    if request.method == 'POST':
        form = VolunteerForm(request.POST)
        if form.is_valid():
                print("Here")
                volunteer = form.save(commit=False)
                volunteer.user = user
                volunteer.save()
                login(request, user)
                return redirect('home')
        else:
            return render(request, 'register2.html', {'form':form, 'type':'Volunteer'})
    return render(request, 'register2.html', {'form':form, 'type':'Volunteer'})



def orgregister(request):
    if request.user.is_authenticated:
        return redirect('home')

    user = User.objects.get(username=request.session['username'])
    form = OrganizationForm()
    if request.method == 'POST':
        
        form = OrganizationForm(request.POST)
        if form.is_valid():
                org = form.save(commit=False)
                org.user = user
                org.save()
                login(request, user)
                return redirect('home')
        else:
            return render(request, 'register2.html', {'form':form})
    return render(request, 'register2.html', {'form':form, 'type':'Organization'})

from django.contrib.auth import logout


def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to the homepage or any other page

@login_required
def profile(request):
    return render(request, 'profile.html')
