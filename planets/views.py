from django.shortcuts import render
from planets.models import Planet
from planets.serializers import PlanetSerializer
from rest_framework import viewsets

class PlanetViewSet(viewsets.ModelViewSet):
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer
