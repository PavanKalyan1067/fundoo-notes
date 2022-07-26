from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from Fundoonotes.models import Notes
from labels.models import Labels
from users.models import User


class TestLabelsAPI(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='a6b6', email='a6b6@gmail.com', password='123Aabc')
        self.label1 = Labels.objects.create(label="hey", user_id=self.user.id)
        self.label2 = Labels.objects.create(label="Hello", user_id=self.user.id)

    def test_create_label(self):
        # Create user
        User.objects.create_user(username='a1b1', email='a1b1@gmail.com', password='123Aabc')
        url = reverse('login')
        # Login successful
        data = {'email': 'a1b1@gmail.com', 'password': '123Aabc'}
        response = self.client.post(url, data)
        token = response.data['data']['tokens']['access']
        data = {
            'label': "hey"
        }
        header = {'Content-Type': 'application/json', 'HTTP_AUTHORIZATION': 'Bearer ' + token}
        response = self.client.get(
            reverse('create-label'),data, format="json", **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_label(self):
        User.objects.create_user(username='a1b1', email='a1b1@gmail.com', password='123Aabc')
        url = reverse('login')
        # Login successful
        data = {'email': 'a1b1@gmail.com', 'password': '123Aabc'}
        response = self.client.post(url, data)
        token = response.data['data']['tokens']['access']
        header = {'Content-Type': 'application/json', 'HTTP_AUTHORIZATION': 'Bearer ' + token}
        notes = Notes.objects.all()
        response = self.client.get(
            reverse('create-label', ), format="json", **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_label(self):
        url = reverse('delete-label', kwargs={'pk': self.label2.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
