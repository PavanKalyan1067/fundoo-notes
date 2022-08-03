from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from Fundoonotes.models import Notes
from labels.models import Labels
from users.models import User


class TestNotesAPI(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='a6b6', email='a6b6@gmail.com', password='123Aabc')
        self.user1 = User.objects.create_user(username='a7b7', email='a7b7@gmail.com', password='123Aabc')
        self.note1 = Notes.objects.create(title='Notes1', description='Something Notes', user_id=self.user.id)
        self.label1 = Labels.objects.create(label="hey", user_id=self.user.id)
        self.note2 = Notes.objects.create(title='Notes2', description='Something Notes', user_id=self.user.id)
        self.note3 = Notes.objects.create(title='Notes3', description='Something Notes', user_id=self.user.id)
        self.note4 = Notes.objects.create(title='Notes4', description='Something Notes', user_id=self.user1.id)

    def test_response_as_create_notes_successfully(self):
        # Create user
        User.objects.create_user(username='a1b1', email='a1b1@gmail.com', password='123Aabc')
        url = reverse('login')
        # Login successful
        data = {'email': 'a1b1@gmail.com', 'password': '123Aabc'}
        response = self.client.post(url, data)
        token = response.data['data']['tokens']['access']
        url = reverse('create-notes')
        data = {
            "title": "Python",
            "description": "learn at 7am",
            "collaborator": [self.user.id],
            "label": [self.label1.id]
        }
        header = {'Content-Type': 'application/json', 'HTTP_AUTHORIZATION': 'Bearer ' + token}
        response = self.client.post(url, data, **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_note(self):
        User.objects.create_user(username='a1b1', email='a1b1@gmail.com', password='123Aabc')
        url = reverse('login')
        # Login successful
        data = {'email': 'a1b1@gmail.com', 'password': '123Aabc'}
        response = self.client.post(url, data)
        token = response.data['data']['tokens']['access']
        header = {'Content-Type': 'application/json', 'HTTP_AUTHORIZATION': 'Bearer ' + token}
        notes = Notes.objects.all()
        response = self.client.get(
            reverse('retrieve', ), format="json", **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_note(self):
        url = reverse('delete-notes', kwargs={'pk': self.note1.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_archive_note(self):
        url = reverse('archive-notes', kwargs={'pk': self.note2.id})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_trash_note(self):
        url = reverse('trash-notes', kwargs={'pk': self.note2.id})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_pin_note(self):
        url = reverse('pin-notes', kwargs={'pk': self.note4.id})
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
