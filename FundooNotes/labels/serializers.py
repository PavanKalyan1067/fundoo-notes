from rest_framework import serializers

from labels.models import Labels


class LabelSerializer(serializers.ModelSerializer):
    """
        Notes Serializer : name,
    """
    name = serializers.CharField(min_length=2, max_length=100, required=True)

    class Meta:
        model = Labels
        fields = ['name']