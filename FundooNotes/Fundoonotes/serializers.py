from rest_framework import serializers

from Fundoonotes.models import Notes


class NotesSerializer(serializers.ModelSerializer):
    """
        Notes Serializer : title, description
    """
    title = serializers.CharField(min_length=4, max_length=400, required=True)
    description = serializers.CharField(min_length=4, max_length=1200, required=True)

    class Meta:
        model = Notes
        fields = ['id', 'title', 'description', 'isArchive', 'isTrash']