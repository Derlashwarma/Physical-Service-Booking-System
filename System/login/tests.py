from django.test import TestCase
from django.urls import reverse
from login.forms import LoginForm
from register.models import CustomUser

class LoginTestCases(TestCase):
    
    def test_login_get(self):
        response = self.client.get(reverse('login:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertIsInstance(response.context['form'], LoginForm)

    def test_empty_inputs(self):
        form_data = {
            'username': '',
            'password': ''
        }
        response = self.client.post(reverse('login:login'), form_data)
        self.assertContains(response, 'This field is required')

    def test_wrong_username_and_password_inputs(self):
        user = CustomUser.objects.create_user(
            username="username1", 
            password="Password1.",
            email='clientuser@example.com',
            is_worker=True
        )
        user = CustomUser.objects.get(username='username1')
        self.assertEqual(user.username, 'username1') 
        self.assertTrue(user.check_password('Password1.')) 

        self.assertTrue(user.is_worker) 

        response = self.client.post(reverse('login:login'), {
            'username': 'wrongusername',
            'password': 'Password1.'
        })
        self.assertContains(response, "Invalid username or password", status_code=200)

        response = self.client.post(reverse('login:login'), {
            'username': 'username1',
            'password': 'wrongpassword'
        })
        self.assertContains(response, "Invalid username or password", status_code=200)
