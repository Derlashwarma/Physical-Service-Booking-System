from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .forms import RegistrationForm
from register.models import CustomUser

class RegistrationTests(TestCase):
    
    def test_register_get(self):
        response = self.client.get(reverse('register:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertIsInstance(response.context['form'], RegistrationForm)

    def test_register_post_valid_form(self):
        form_data = {
            'username': 'testuser',
            'password': 'passworD.123',
            'confirm_password': 'passworD.123',
            'email': 'testuser@example.com',
            'is_worker': True,
        }
        response = self.client.post(reverse('register:register'), form_data)
        self.assertRedirects(response, reverse('register:register_success'))

    def test_register_post_passwords_do_not_match(self):
        form_data = {
            'username': 'testuser',
            'password': 'passworD.123',
            'confirm_password': 'passworD.1s23',
            'email': 'testuser@example.com',
            'is_worker': True,
        }
        response = self.client.post(reverse('register:register'), form_data)
        self.assertContains(response, 'Passwords do not match')
        self.assertEqual(response.status_code, 200)

        with self.assertRaises(get_user_model().DoesNotExist):
            get_user_model().objects.get(username='testuser')

    def test_register_post_invalid_form(self):
        form_data = {
            'username': '',
            'password': 'passworD.123',
            'confirm_password': 'passworD.123',
            'email': 'testuser@example.com',
            'is_worker': True,
        }
        response = self.client.post(reverse('register:register'), form_data)
        self.assertContains(response, 'This field is required')
        self.assertEqual(response.status_code, 200)

    def test_register_success_worker(self):
        self.client.post(reverse('register:register'), {
            'username': 'workeruser',
            'password': 'passworD.123',
            'confirm_password': 'passworD.123',
            'email': 'workeruser@example.com',
            'is_worker': True,
        })
        response = self.client.get(reverse('register:register_success'))
        self.assertContains(response, "local professionals")

    def test_register_success_client(self):
        response = self.client.post(reverse('register:register'), {
            'username': 'clientuser',
            'password': 'passworD.123',
            'confirm_password': 'passworD.123',
            'email': 'clientuser@example.com',
            'is_worker': False,
        })
        self.assertRedirects(response, reverse('register:register_success'))
        user = CustomUser.objects.get(username='clientuser')
        self.assertEqual(user.username, 'clientuser')
        self.assertTrue(user.check_password('passworD.123')) 
        self.assertFalse(user.is_worker)
