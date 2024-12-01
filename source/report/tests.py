from django.test import TestCase
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
        self.crisis_data = {
            'name': 'Test Crisis',
            'description': 'Test Description',
            'severity': '8',
            'latitude': '40.7128',
            'longitude': '-74.0060'
        }

    def test_report_page_access(self):
        # Test that the 'home' page renders correctly
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_dashboard_access(self):
        # Test that the 'incidents' page renders correctly
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('incidents'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'incidents.html')

    def test_report_submission(self):
        # Test the POST request for reporting a crisis
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('home'), self.crisis_data)
        self.assertEqual(response.status_code, 302)  # Redirects after submission
        self.assertEqual(Crisis.objects.count(), 1)  # Crisis should be created