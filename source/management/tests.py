from django.test import TestCase
from django.contrib.auth.models import User
from .models import Organization, Volunteer, Resource, Task
from report.models import Crisis
from django.urls import reverse


class ModelsTestCase(TestCase):

    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username='org_user', password='password123', first_name='Org', last_name='User')
        self.user2 = User.objects.create_user(username='vol_user', password='password123', first_name='Vol', last_name='User')
        
        # Create an organization
        self.organization = Organization.objects.create(user=self.user1, domain="Healthcare", level="N")
        
        # Create a volunteer
        self.volunteer = Volunteer.objects.create(user=self.user2, organization=self.organization, age=30, sex='M', skills="First Aid, Rescue Operations")
        
        # Create a crisis (mocking Crisis model)
        self.crisis = Crisis.objects.create(name="Flood in Area A", description="Severe flooding requiring immediate attention.")
        
        # Create a resource
        self.resource = Resource.objects.create(organization=self.organization, name="Food Packets", quantity="100")
        
        # Create a task
        self.task = Task.objects.create(name="Distribute Food", description="Deliver food packets to affected areas.", crisis=self.crisis, assignee=self.volunteer)

    def test_organization_creation(self):
        self.assertEqual(str(self.organization), "Org User")
        self.assertEqual(self.organization.domain, "Healthcare")
        self.assertEqual(self.organization.level, "N")

    def test_volunteer_creation(self):
        self.assertEqual(str(self.volunteer), "Vol User")
        self.assertEqual(self.volunteer.age, 30)
        self.assertEqual(self.volunteer.sex, "M")
        self.assertEqual(self.volunteer.skills, "First Aid, Rescue Operations")
        self.assertEqual(self.volunteer.organization, self.organization)

    def test_resource_creation(self):
        self.assertEqual(str(self.resource), "Food Packets")
        self.assertEqual(self.resource.organization, self.organization)
        self.assertEqual(self.resource.quantity, "100")

    def test_task_creation(self):
        self.assertEqual(self.task.name, "Distribute Food")
        self.assertEqual(self.task.description, "Deliver food packets to affected areas.")
        self.assertEqual(self.task.crisis, self.crisis)
        self.assertEqual(self.task.assignee, self.volunteer)
        self.assertEqual(self.task.status, "Unsolved")  # Default status

    def test_task_status_update(self):
        self.task.status = "I"
        self.task.save()
        self.assertEqual(self.task.status, "I")

    def test_resource_deletion(self):
        resource_id = self.resource.pk
        self.resource.delete()
        self.assertFalse(Resource.objects.filter(pk=resource_id).exists())

    def test_task_deletion(self):
        task_id = self.task.pk
        self.task.delete()
        self.assertFalse(Task.objects.filter(pk=task_id).exists())

    def test_volunteer_on_delete_set_null(self):
        task_id = self.task.pk
        self.volunteer.delete()
        task = Task.objects.get(pk=task_id)
        self.assertIsNone(task.assignee)

    # Test Profile Edit
    def test_edit_volunteer_profile(self):
        self.client.login(username='vol_user', password='password123')
        response = self.client.get(reverse('edit_volunteer_profile'))
        self.assertEqual(response.status_code, 200)
        
        data = {'age': 31, 'sex': 'M', 'skills': 'First Aid, Rescue Operations, CPR'}
        response = self.client.post(reverse('edit_volunteer_profile'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after update
        self.volunteer.refresh_from_db()
        self.assertEqual(self.volunteer.age, 31)

    def test_edit_organization_profile(self):
        self.client.login(username='org_user', password='password123')
        response = self.client.get(reverse('edit_organization_profile'))
        self.assertEqual(response.status_code, 200)
        
        data = {'domain': 'Emergency Response', 'level': 'A'}
        response = self.client.post(reverse('edit_organization_profile'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after update
        self.organization.refresh_from_db()
        self.assertEqual(self.organization.domain, 'Emergency Response')

    # Test Crisis Task Management
    def test_accept_task(self):
        self.client.login(username='vol_user', password='password123')
        response = self.client.post(reverse('accept_task', args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect after accepting task
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, "In-Progress")
        self.assertEqual(self.task.assignee, self.volunteer)

    def test_mark_task_done(self):
        self.client.login(username='vol_user', password='password123')
        self.task.status = "In-Progress"
        self.task.save()
        response = self.client.post(reverse('mark_task_done', args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect after marking as done
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, "Solved")

    def test_logout(self):
        # Test logout
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout

    def test_edit_volunteer_profile(self):
        self.client.login(username='vol_user', password='password123')
        response = self.client.get(reverse('edit_volunteer_profile'))
        self.assertEqual(response.status_code, 200)  # Profile editing page accessible
        
        data = {'age': 31, 'sex': 'M', 'skills': 'First Aid, CPR'}
        response = self.client.post(reverse('edit_volunteer_profile'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after updating profile
        self.volunteer.refresh_from_db()
        self.assertEqual(self.volunteer.age, 31)

    def test_edit_organization_profile(self):
        self.client.login(username='org_user', password='password123')
        response = self.client.get(reverse('edit_organization_profile'))
        self.assertEqual(response.status_code, 200)  # Profile editing page accessible
        
        data = {'domain': 'Emergency Response', 'level': 'A'}
        response = self.client.post(reverse('edit_organization_profile'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after updating profile
        self.organization.refresh_from_db()
        self.assertEqual(self.organization.domain, 'Emergency Response')


