from rest_framework import serializers

from Fundoonotes.models import Notes
from labels.models import Labels


class NotesSerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=4, max_length=400, required=True)
    description = serializers.CharField(min_length=4, max_length=1200, required=True)

    class Meta:
        model = Notes
        fields = '__all__'
        read_only_fields = ['id', 'user', 'isTrash']

    def create(self, validated_data):
        user = validated_data['user_id']
        collaborator = validated_data.pop('collaborator')
        label = validated_data.pop('label')
        note = Notes.objects.create(**validated_data)
        note.collaborator.set(collaborator)
        note.label.set(label)
        note.save()
        return note


class LabelSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Labels
        fields = ['label', 'id']


class GetNoteSerializer(serializers.ModelSerializer):
    label = LabelSerializer1(many=True)
    reminder = serializers.TimeField(format="%H:%M", required=False)

    class Meta:
        model = Notes
        fields = ['user', 'title', 'description', 'reminder', 'isArchive', 'isTrash', 'isPinned',
                  'collaborator', 'label']
        read_only_fields = ['id', 'user']


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
