from rest_framework import serializers

from labels.models import Labels


class LabelSerializer(serializers.ModelSerializer):

    label = serializers.CharField(min_length=2, max_length=100, required=True)

    class Meta:
        model = Labels
        fields = '__all__'
        read_only_fields = ['id', 'label_id']
