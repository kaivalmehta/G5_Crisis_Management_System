from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Crisis
from management.models import Organization

class CrisisReportTests(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        self.organization = Organization.objects.create(user=self.user)
        
        # Create a crisis report for later tests
        self.crisis = Crisis.objects.create(
            name="Test Crisis",
            description="A test crisis description.",
            severitylvl=5,
            lat=40.7128,
            lon=-74.0060,
            currentstatus='R'  # 'R' stands for Reported status
        )

        self.client = Client()

    def test_report_page_access(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_guidelines_page_access(self):
        response = self.client.get(reverse('guidelines'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'guidelines.html')

    def test_donation_page_access(self):
        response = self.client.get(reverse('donate'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'donate.html')

    def test_dashboard_access(self):
        # Test that the 'incidents' page renders correctly
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('incidents'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'incidents.html')

    def test_respond_view_authenticated(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Respond to the crisis
        response = self.client.get(reverse('respond', args=[self.crisis.crisisID]))

        # Reload the crisis object
        self.crisis.refresh_from_db()

        # Assert the crisis was assigned to the user's organization
        self.assertEqual(self.crisis.assignee, self.organization)
        self.assertEqual(self.crisis.currentstatus, 'I')
        self.assertRedirects(response, reverse('incidents'))

    def test_respond_view_unauthenticated(self):
        # Attempt to respond without logging in
        response = self.client.get(reverse('respond', args=[self.crisis.crisisID]))

        # Assert redirection to the login page
        self.assertRedirects(response, reverse('login'))

    def test_solve_view_authenticated(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Assign the crisis to the organization
        self.crisis.assignee = self.organization
        self.crisis.currentstatus = 'I'
        self.crisis.save()

        # Solve the crisis
        response = self.client.get(reverse('solved', args=[self.crisis.crisisID]))

        # Reload the crisis object
        self.crisis.refresh_from_db()

        # Assert the crisis status was updated and assignee removed
        self.assertEqual(self.crisis.currentstatus, 'S')
        self.assertIsNone(self.crisis.assignee)
        self.assertRedirects(response, reverse('incidents'))

    def test_solve_view_unauthenticated(self):
        # Attempt to solve without logging in
        response = self.client.get(reverse('solved', args=[self.crisis.crisisID]))

        # Assert redirection to the login page
        self.assertRedirects(response, reverse('login'))