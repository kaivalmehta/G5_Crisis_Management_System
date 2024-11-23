from django.forms import ModelForm
from .models import Organization, Volunteer, Resource,Task
from django.forms import CheckboxSelectMultiple, TextInput, NumberInput, Select, SelectMultiple


class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        exclude = ['user']
        widgets = {
            'domain': TextInput(attrs={"class":"form-control my-2 mb-3"}),
            'level': Select(attrs={"class":"form-select my-2 mb-3"}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['domain'].required = True
        self.fields['level'].required = True


class VolunteerForm(ModelForm):
    class Meta:
        model = Volunteer
        exclude = ['user']
        widgets = {
            'organization': Select(attrs={"class":"form-select my-2 mb-3"}),
            'age': NumberInput(attrs={"class":"form-control my-2 mb-3"}),
            'sex': Select(attrs={"class":"form-select my-2 mb-3"}),
            'skills': TextInput(attrs={"class":"form-control my-2 mb-3"}),
                                
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True


class ResourceForm(ModelForm):
    class Meta:
        model = Resource
        exclude = ['resourceID', 'organization']
        widgets = {
            'name': TextInput(attrs={"class":"form-control my-2 mb-3"}),
            'quantity':TextInput(attrs={"class":"form-control my-2 mb-3"})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True

class TaskForm(ModelForm):
    class Meta:
        model=Task
        exclude=['taskID','assignee','status','crisis']
        widgets={
            'name':  TextInput(attrs={"class":"form-control my-2 mb-3"}),
            'description':TextInput(attrs={"class":"form-control my-2 mb-3"}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        