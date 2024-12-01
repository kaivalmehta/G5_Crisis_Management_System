from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import uuid
# Create your models here.

class Organization(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    domain = models.CharField(max_length=256, blank=True)
    level = models.CharField(max_length=1, blank=True,
        choices=[
            ('L', 'Local'),
            ('R', 'Regional'),
            ('N','National'),
            ('I', 'International')
        ]
    )
    def __str__(self):
        return str(self.user.get_full_name())



class Volunteer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, blank=True, null=True, default=None)
    age = models.PositiveSmallIntegerField(blank=True, null=True)
    sex = models.CharField(max_length=1, blank=True, null=True,
        choices=[
            ('M', 'Male'),
            ('F', 'Female'),
            ('O', 'Other')
        ])
    skills = models.TextField(blank=True)

    def __str__(self):
        return str(self.user.get_full_name())
    

class Resource(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    resourceID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    quantity = models.CharField(max_length=32)

    def __str__(self):
        return str(self.name)

class Task(models.Model):
    taskID=models.UUIDField(primary_key = True, default = uuid.uuid4,editable = False)
    name=models.CharField(max_length=100)
    description = models.TextField()
    crisis = models.ForeignKey('report.Crisis', on_delete=models.CASCADE, related_name="tasks")
    assignee = models.ForeignKey(Volunteer, on_delete=models.SET_NULL, blank=True, null=True,default="")
    status= models.CharField(max_length=1,
        choices=[
            ('U', 'Unsolved'),
            ('I', 'In Progress'),
            ('S', 'Solved')
        ],default='Unsolved'
    )  