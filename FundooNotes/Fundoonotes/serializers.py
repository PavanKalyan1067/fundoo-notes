from rest_framework import serializers

from Fundoonotes.models import Notes
from labels.models import Labels


class NotesSerializer(serializers.ModelSerializer):
    """
        Notes Serializer : title, description
    """
    title = serializers.CharField(min_length=4, max_length=400, required=True)
    description = serializers.CharField(min_length=4, max_length=1200, required=True)

    class Meta:
        model = Notes
        fields = ['id', 'title', 'description', 'isArchive', 'isTrash', 'collaborator']


class NoteSerializer(serializers.ModelSerializer):
    reminder = serializers.TimeField(format="%H:%M", required=False)

    class Meta:
        model = Notes
        fields = '__all__'
        read_only_fields = ['id', 'user', 'trash']

    def create(self, validated_data):
        user = validated_data['user']
        collaborators = validated_data.pop('collaborators')
        try:
            labels = validated_data['label']
        except KeyError:
            labels = []
        note = Notes.objects.create(**validated_data)
        note.collaborators.set(collaborators)
        note.save()
        for label in labels:
            Labels.objects.get_or_create(label_id=user, label=label)
        return note
