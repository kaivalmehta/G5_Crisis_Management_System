from django.urls import path
from . import views

#localhost:8000/report/

#URL CONFIGURATION
urlpatterns = [
    path('',views.report,name="report"),
]