from django.urls import path
from . import views

#localhost:8000/report/

#URL CONFIGURATION
urlpatterns = [
    path('',views.report,name="home"),
    path('incidents/',views.dashboard,name="incidents"),
    path('respond/<slug:cID>',views.respond,name="respond"),
    path('solved/<slug:cID>',views.solve,name="solved"),
]