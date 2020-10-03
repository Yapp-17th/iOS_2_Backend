from django.shortcuts import render
from trashcans.models import Trashcan
from trashcans.serializers import TrashcanSerializer
from rest_framework import viewsets

class TrashcanViewSet(viewsets.ModelViewSet):
    queryset = Trashcan.objects.all()
    serializer_class = TrashcanSerializer