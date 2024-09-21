from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def notification(request):
    return render(request, 'hello.html',{'crisis':'Earthquake'})
