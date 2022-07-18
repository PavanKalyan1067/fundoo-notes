from django.contrib.auth.models import User
from rest_framework import serializers

import labels
from Fundoonotes.models import Notes
from labels.models import Labels
from labels.serializers import LabelSerializer


class NotesSerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=4, max_length=400, required=True)
    description = serializers.CharField(min_length=4, max_length=1200, required=True)

    class Meta:
        model = Notes
        fields = '__all__'
        read_only_fields = ['id', 'user', 'isTrash']

    def create(self, validated_data):
        collaborator = validated_data.pop('collaborator')
        note = Notes.objects.create(**validated_data)
        note.collaborator.set(collaborator)
        note.save()
        return note


class TrashSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['id', 'title', 'description', 'isTrash']
        read_only_fields = ['id', 'title']


class PinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['id', 'title', 'description', 'isPinned']
        read_only_fields = ['id', 'title']
