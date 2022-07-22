import json
from unittest import TestCase

import requests
from django.urls import reverse, resolve

from users.views import LoginAPIView


class TestUrls(TestCase):

    def test_login_url(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, LoginAPIView)


class TestCasesForLogin(TestCase):
    def test_for_email_password_all_details_given(self):
        ENDPOINT = 'user/api/login/'
        url = 'http://127.0.0.1:8000/' + ENDPOINT
        data = {"email": "a1b1@gmail.com", "password": "123Aabc"}
        headers = {'Content-Type': 'application/json'}
        response_ = requests.post(url, data=json.dumps(data), headers=headers)
        assert response_.status_code == 200

    def test_for_password_all_not_given(self):
        ENDPOINT = 'user/api/login/'
        url = 'http://127.0.0.1:8000/' + ENDPOINT
        data = {"email": "a1b1@gmail.com"}
        headers = {'Content-Type': 'application/json'}
        response_ = requests.post(url, data=json.dumps(data), headers=headers)
        assert response_.status_code == 400

    def test_for_email_all_not_given(self):
        ENDPOINT = 'user/api/login/'
        url = 'http://127.0.0.1:8000/' + ENDPOINT
        data = {"password": "123Aabc"}
        headers = {'Content-Type': 'application/json'}
        response_ = requests.post(url, data=json.dumps(data), headers=headers)
        assert response_.status_code == 400
