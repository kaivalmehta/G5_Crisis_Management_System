# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .forms import VolunteerForm,OrganizationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Volunteer, Organization, Resource
from .forms import ResourceForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Resource

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
def resources(request):
    # Check if the user is an organization
    organization = Organization.objects.filter(user=request.user).first()
    if organization:
        resources = Resource.objects.filter(organization=organization)
        return render(request, 'resources.html', {'resources': resources, 'profile_type': 'organization'})
    else:
        return render(request, 'resources.html', {'profile_type': 'volunteer'})

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def profile(request):
    user = request.user
    context = {}

    # Check if user is a Volunteer
    try:
        volunteer = Volunteer.objects.get(user=user)
        context['profile_type'] = 'volunteer'
        context['profile'] = volunteer
    except Volunteer.DoesNotExist:
        # Check if user is an Organization
        try:
            organization = Organization.objects.get(user=user)
            context['profile_type'] = 'organization'
            context['profile'] = organization
        except Organization.DoesNotExist:
            context['profile_type'] = None

    return render(request, 'profile.html', context)

@login_required
def edit_volunteer_profile(request):
    user = request.user
    try:
        volunteer = Volunteer.objects.get(user=user)
    except Volunteer.DoesNotExist:
        return redirect('profile')

    if request.method == 'POST':
        age = request.POST.get('age')
        sex = request.POST.get('sex')
        skills = request.POST.get('skills')

        volunteer.age = age
        volunteer.sex = sex
        volunteer.skills = skills
        volunteer.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')

    return render(request, 'edit_volunteer_profile.html', {'volunteer': volunteer})

@login_required
def edit_organization_profile(request):
    user = request.user
    try:
        organization = Organization.objects.get(user=user)
    except Organization.DoesNotExist:
        return redirect('profile')

    if request.method == 'POST':
        domain = request.POST.get('domain')
        level = request.POST.get('level')

        organization.domain = domain
        organization.level = level
        organization.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')

    return render(request, 'edit_organization_profile.html', {'organization': organization})

@login_required
def add_resource(request):
    # Restrict access to organizations only
    organization = Organization.objects.filter(user=request.user).first()
    if not organization:
        return redirect('resources')  # Redirect to the resources page with restricted access
    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.organization = organization
            resource.save()
            return redirect('resources')
    else:
        form = ResourceForm()
    return render(request, 'add_resource.html', {'form': form})

def delete_resource(request, resource_id):
    if request.method == "POST":
        resource = get_object_or_404(Resource, resourceID=resource_id)
        resource.delete()
        return JsonResponse({"success": True, "message": "Resource deleted successfully!"})
    return JsonResponse({"success": False, "message": "Invalid request."})


def volunteer_list(request):
    volunteers = Volunteer.objects.all()
    return render(request, 'volunteer.html', {'volunteers': volunteers, 'organizations': Organization})