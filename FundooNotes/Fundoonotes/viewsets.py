from rest_framework import viewsets
from . import models
from . import serializers


class NoteViewSet(viewsets.ModelViewSet):
    queryset = models.Notes.objects.all()
    serializer_class = serializers.NotesSerializer
