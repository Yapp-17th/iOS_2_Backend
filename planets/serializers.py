from planets.models import Planet
from rest_framework import serializers

class PlanetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planet
        fields = '__all__'