from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Organization)
admin.site.register(Volunteer)
admin.site.register(Resource)
admin.site.register(Task)