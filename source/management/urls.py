# urls.py
from django.urls import path,include
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
    path('tasks/<slug:crisis_id>',views.crisis_tasks,name='crisis_tasks'),
    path('task/<slug:task_id>/delete/', views.delete_task, name='delete_task'),
    path('tasks/<slug:crisis_id>/add-task/',views.task_form,name='task_form'),
    path('task/<slug:task_id>/accept/', views.accept_task, name='accept_task'),
    path('task/<slug:task_id>/done/', views.mark_task_done, name='mark_task_done'),
    path('volunteers/', views.volunteer_list, name='volunteer'),
]
