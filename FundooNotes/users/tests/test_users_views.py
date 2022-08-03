from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from users.models import User


class TestsCasesForRegistration(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='a6b6', email='a6b6@gmail.com', password='123Aabc')

    def test_for_registration_email_password_all_details_given(self):
        User.objects.create_user(username='a1b1', email='a1b1@gmail.com', password='123Aabc')
        url = reverse('login')
        # Login successful
        data = {'email': 'a1b1@gmail.com', 'password': '123Aabc'}
        response = self.client.post(url, data)
        token = response.data['data']['tokens']['access']
        url = reverse('create-notes')
        data = {
            "first_name": "a4",
            "last_name": "b4",
            "username": "a4b4",
            "email": "a4b4@gmail.com",
            "password": "A1234abc",
            "confirm_password": "A1234abc"
        }
        header = {'Content-Type': 'application/json', 'HTTP_AUTHORIZATION': 'Bearer ' + token}
        response = self.client.post(url, data, **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_user(self):
        url = reverse('login', )
        data = {"email": "a1b1@gmail.com", "password": "123Aabc"}
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
