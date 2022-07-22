import json
from unittest import TestCase
import requests
from django.urls import reverse
from rest_framework import status


class TestNotes(TestCase):

    # def setUp(self):
    # self.note1 = Notes.objects.create(title='Gym', description='go to gym at morning 6 ')
    # self.note2 = Notes.objects.create(title='Study', description='study daily')

    def test_create_note(self):
        url = reverse('create-notes')
        data = {'title': 'notes', 'description': 'Created a New Note'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestCasesForCreateNote(TestCase):

    def test__title_note_given(self):
        ENDPOINT = 'notes/api/create/'
        url = 'http://127.0.0.1:8000/' + ENDPOINT
        data = {
            "title": "jnfy",
            "description": "yy uhu",
            "collaborator": [22],
            "label": [2]
        }
        headers = {'Accept': 'application/json'}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        assert response.status_code == 401

    def test__note_not_given(self):
        ENDPOINT = 'notes/api/create/'
        url = 'http://127.0.0.1:8000/' + ENDPOINT
        data = {"title": "Test Case for Create Note"}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        assert response.status_code, status.HTTP_401_UNAUTHORIZED
