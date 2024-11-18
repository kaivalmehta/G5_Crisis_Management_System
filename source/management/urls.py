# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register/volunteer', views.volregister, name='volregister'),
    path('register/organization', views.orgregister, name='orgregister'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('profile/', views.profile, name='profile'),
    path('profile/edit/volunteer/', views.edit_volunteer_profile, name='edit_volunteer_profile'),
    path('profile/edit/organization/', views.edit_organization_profile, name='edit_organization_profile'),

    path('resources/', views.resources, name='resources'),
    path('resources/add/', views.add_resource, name='add_resource'),
    path('delete_resource/<uuid:resource_id>/', views.delete_resource, name='delete_resource'),

    path('volunteers/', views.volunteer_list, name='volunteer'),
]
