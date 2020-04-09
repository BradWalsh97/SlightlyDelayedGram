from django.test import TestCase
from django.urls import reverse
#from unittest import TestCase

# Create your tests here.
class UsersViewsTest(TestCase):
    def test_home(self):
        response = self.client.get(reverse('users-home'))
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)

    def test_trending(self):
        response = self.client.get(reverse('trending'))
        self.assertEqual(response.status_code, 200)

    def test_upload(self):
        response = self.client.get(reverse('upload'))
        self.assertEqual(response.status_code, 302) # Code 302 since login is required and user is not logged in

    def test_register(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
    
    def test_profile(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302) # Code 302 since login is required and user is not logged in
