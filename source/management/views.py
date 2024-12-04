# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .forms import VolunteerForm,OrganizationForm,TaskForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Volunteer, Organization, Resource , Task
from .forms import ResourceForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import JsonResponse,HttpResponseForbidden
from .models import Resource
from report.models import Crisis

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

        user = User(first_name=request.POST['name'], username=request.POST['email'],email=request.POST['email'])
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
    assigned_crises=[]
    # Check if user is a Volunteer
    try:
        volunteer = Volunteer.objects.get(user=user)
        context['profile_type'] = 'volunteer'
        context['profile'] = volunteer
        organizationid=volunteer.organization
        organization=Organization.objects.get(user=organizationid.user)
        assigned_crises=Crisis.objects.filter(assignee=organization)
        context['assigned_crises']=assigned_crises
    except Volunteer.DoesNotExist:
        # Check if user is an Organization
        try:
            organization = Organization.objects.get(user=user)
            context['profile_type'] = 'organization'
            context['profile'] = organization
            assigned_crises = Crisis.objects.filter(assignee=request.user.organization)
            context['assigned_crises']=assigned_crises
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
    organization = Organization.objects.filter(user=request.user).first()  # Get the first matching organization
    volunteers = Volunteer.objects.filter(organization=organization) # Check if organization exists
    return render(request, 'volunteer.html', {'volunteers': volunteers})


@login_required
def crisis_tasks(request, crisis_id):
    crisis = get_object_or_404(Crisis, crisisID=crisis_id)
    tasks = Task.objects.filter(crisis=crisis)   
    return render(request, 'task.html', {'crisis': crisis, 'tasks': tasks})


@login_required
def task_form(request, crisis_id):
    crisis = get_object_or_404(Crisis, crisisID=crisis_id)
    form = TaskForm()  

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.crisis = crisis 
            task.save()
            return redirect('crisis_tasks',crisis_id=crisis.crisisID)  

    return render(request, 'task_form.html', {'form': form, 'crisis': crisis})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, taskID=task_id)
    if request.user.organization:
        task.delete()
        return redirect('crisis_tasks', crisis_id=task.crisis.crisisID)  # Redirect to the crisis tasks page
    else:
        return HttpResponseForbidden("You do not have permission to delete this task.")
    
@login_required
def accept_task(request, task_id):
    task = get_object_or_404(Task, taskID=task_id)
    try:
        volunteer = Volunteer.objects.get(user=request.user)
    except Volunteer.DoesNotExist:
        return HttpResponseForbidden("Only volunteers can accept tasks.")

    task.assignee = volunteer
    task.status = 'In-Progress'
    task.save()
    return redirect('crisis_tasks',crisis_id=task.crisis.crisisID)

@login_required
def mark_task_done(request, task_id):
    task = get_object_or_404(Task, taskID=task_id)
    if task.assignee and task.assignee.user == request.user:
        task.status = 'Solved'
        task.save()
        return redirect('crisis_tasks',crisis_id=task.crisis.crisisID)  # Adjust to your tasks list or detail view URL
    else:
        return HttpResponseForbidden("You are not assigned to this task.")
    
@login_required
def delete_user(request):
    if request.method == "POST":
        # Delete the authenticated user
        user = request.user
        user.delete()
        # Redirect to a page after user deletion
        return redirect('home')