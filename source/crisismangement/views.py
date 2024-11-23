from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def home(request):
    return render(request, 'home.html')

def guidelines(request):
    return render(request, 'guidelines.html')

def donate(request):
    return render(request, 'donate.html')
