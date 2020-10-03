from quests.models import Quest
from rest_framework import serializers

class QuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quest
        fields = '__all__'