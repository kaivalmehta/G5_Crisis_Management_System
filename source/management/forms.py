from django.forms import ModelForm
from .models import Organization, Volunteer, Resource,Task
from django.forms import CheckboxSelectMultiple, TextInput, NumberInput, Select, SelectMultiple,IntegerField,CharField


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
    age = IntegerField(
        widget=NumberInput(attrs={"class": "form-control my-2 mb-3"}),
        min_value=18,
        max_value=75,
        error_messages={
            'required': 'This field is required.',
            'invalid': 'Enter a valid number.',
            'min_value': 'Age must be at least 18.',
            'max_value': 'Age cannot exceed 75.'
        }
    )

    class Meta:
        model = Volunteer
        exclude = ['user']
        widgets = {
            'organization': Select(attrs={"class": "form-select my-2 mb-3"}),
            'sex': Select(attrs={"class": "form-select my-2 mb-3"}),
            'skills': TextInput(attrs={"class": "form-control my-2 mb-3"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True


class ResourceForm(ModelForm):
    name = CharField(
        max_length=50,  # Enforce the max_length constraint
        widget=TextInput(attrs={"class": "form-control my-2 mb-3"}),
        error_messages={
            'max_length': 'Name cannot exceed 50 characters.',
            'required': 'This field is required.',
        }
    )
    quantity = IntegerField(
        widget=NumberInput(attrs={"class": "form-control my-2 mb-3"}),
        min_value=1,
        error_messages={
            'required': 'This field is required.',
            'invalid': 'Enter a valid number.',
            'min_value': 'Quantity must be a positive integer.'
        }
    )

    class Meta:
        model = Resource
        exclude = ['resourceID', 'organization']

class TaskForm(ModelForm):
    name = CharField(
        max_length=50,
        widget=TextInput(attrs={"class": "form-control my-2 mb-3"}),
        error_messages={
            'required': 'This field is required.',
            'max_length': 'Name cannot exceed 50 characters.',
        }
    )
    description = CharField(
        max_length=255,
        required=False,  
        widget=TextInput(attrs={"class": "form-control my-2 mb-3"}),
        error_messages={
            'max_length': 'Description cannot exceed 255 characters.',
        }
    )

    class Meta:
        model = Task
        exclude = ['taskID', 'assignee', 'status', 'crisis']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True