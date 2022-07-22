import json
from unittest import TestCase
import requests
from rest_framework import status
from Fundoonotes.models import User


class UserRegisterTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='me', email='a1b11@gmail.com', password='meA123')
        self.user2 = User.objects.create(username='you', email='you@gmail.com', password='youU123')

    def test_create_user(self):
        user = self.user1
        user.save()
        self.assertEqual(str(user), 'a1b11@gmail.com')


class TestsCasesForRegistration(TestCase):

    def test_for_registration_email_password_all_details_given(self):
        ENDPOINT = 'user/api/register/'
        url = 'http://127.0.0.1:8000/' + ENDPOINT
        data = {
            "first_name": "v1",
            "last_name": "v1",
            "username": "v v",
            "email": "vishnulucky229@gmail.com",
            "password": "A1234abc",
            "confirm_password": "A1234abc"
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
