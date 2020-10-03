from trashcans.models import Trashcan
from rest_framework import serializers

class TrashcanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trashcan
        fields = '__all__'