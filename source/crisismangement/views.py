from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def home(request):
    return render(request, 'home.html')

from django.urls import reverse
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm

def donate(request):
    paypal_dict = {
        "business": "jashshah780@gmail.com",
        "amount": "10.00",
        "item_name": "donate-to-crisis",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "donate.html", context)



def guidelines(request):
    return render(request, 'guidelines.html')

