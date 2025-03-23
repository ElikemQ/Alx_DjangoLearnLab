from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Profile

# Create your tests here.

class UserAuthenticationTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.profile = Profile.objects.create(user=self.user)

    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'password123',
            'password2': 'password123',
            'email': 'newuser@example.com'
        })
        self.assertEqual(response.status_code, 302)  
        user = User.objects.get(username='newuser')
        self.assertIsNotNone(user)

    def test_user_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password123',
        })
        self.assertEqual(response.status_code, 200)  
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200) 

    def test_user_logout(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))  
    def test_profile_edit(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('profile'), {
            'username': 'testuser',
            'email': 'updated@example.com',
            'first_name': 'Updated',
            'last_name': 'User',
            'bio': 'Updated bio content.',
        })
        self.assertEqual(response.status_code, 302)  
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'updated@example.com')
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'User')

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.bio, 'Updated bio content.')
