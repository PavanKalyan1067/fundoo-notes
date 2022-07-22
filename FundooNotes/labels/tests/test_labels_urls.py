from unittest import TestCase

from django.urls import reverse, resolve
from labels.views import LabelAPIView, UpdateLabelsAPIView, DeleteAPIView


class TestLabelUrls(TestCase):

    def test_label_create_url(self):
        url = reverse('create-label')
        self.assertEqual(resolve(url).func.view_class, LabelAPIView)

    def test_label_update_url(self):
        url = reverse('update-label', kwargs={'pk': 2})
        self.assertEqual(resolve(url).func.view_class, UpdateLabelsAPIView)

    def test_label_delete_url(self):
        url = reverse('delete-label', kwargs={'pk': 10})
        self.assertEqual(resolve(url).func.view_class, DeleteAPIView)
