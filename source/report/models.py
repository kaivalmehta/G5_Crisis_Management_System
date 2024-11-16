from django.db import models
import uuid
from django.utils import timezone
from management.models import Organization

# Create your models here.

class Crisis(models.Model):
    crisisID = models.UUIDField(primary_key = True, default = uuid.uuid4,editable = False)
    name = models.CharField(max_length=256)
    description = models.TextField()
    severitylvl = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True, editable=False)
    assignee = models.ForeignKey(Organization, on_delete=models.SET_NULL, blank=True, null=True) 
    lat = models.DecimalField(max_digits=9, decimal_places=6,null=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6,null=True)
    currentstatus= models.CharField(max_length=1,
        choices=[
            ('R', 'Reported'),
            ('I', 'In Progress'),
            ('S', 'Solved')
        ]
    )  
    def __str__(self):
        return self.name

