from unittest import TestCase

from django.urls import reverse, resolve
from Fundoonotes.views import CreateAPIView, ArchiveNotesAPIView, AllArchiveNotesAPIView, AllTrashNotesAPIView, \
    TrashNotesAPIView, AllPinNotesAPIView, PinNotesAPIView, CollaboratedNoteView, LabelNoteView, UpdateNotesAPIView, \
    DeleteAPIView, RetrieveAPIView


class TestUrls(TestCase):

    def test_note_create_url(self):
        url = reverse('create-notes')
        self.assertEqual(resolve(url).func.view_class, CreateAPIView)

    def test_note_retrieve_url(self):
        url = reverse('retrieve')
        self.assertEqual(resolve(url).func.view_class, RetrieveAPIView)

    def test_note_update_url(self):
        url = reverse('update-notes', kwargs={'pk': 2})
        self.assertEqual(resolve(url).func.view_class, UpdateNotesAPIView)

    def test_note_delete_url(self):
        url = reverse('delete-notes', kwargs={'pk': 10})
        self.assertEqual(resolve(url).func.view_class, DeleteAPIView)

    def test_all_note_archive_url(self):
        url = reverse('all-archive-notes')
        self.assertEqual(resolve(url).func.view_class, AllArchiveNotesAPIView)

    def test_all_note_trash_url(self):
        url = reverse('all-trash-notes')
        self.assertEqual(resolve(url).func.view_class, AllTrashNotesAPIView)

    def test_all_note_pin_url(self):
        url = reverse('all-pin-notes')
        self.assertEqual(resolve(url).func.view_class, AllPinNotesAPIView)

    def test_pin_note_url(self):
        url = reverse('pin-notes', kwargs={'pk': 20})
        self.assertEqual(resolve(url).func.view_class, PinNotesAPIView)

    def test_trash_note_url(self):
        url = reverse('trash-notes', kwargs={'pk': 25})
        self.assertEqual(resolve(url).func.view_class, TrashNotesAPIView)

    def test_archive_note_url(self):
        url = reverse('archive-notes', kwargs={'pk': 40})
        self.assertEqual(resolve(url).func.view_class, ArchiveNotesAPIView)

    def test_collaborate_note_url(self):
        url = reverse('collaborated-note')
        self.assertEqual(resolve(url).func.view_class, CollaboratedNoteView)

    def test_label_note_url(self):
        url = reverse('label-note')
        self.assertEqual(resolve(url).func.view_class, LabelNoteView)
