import csv

from rest_framework.decorators import api_view
from rest_framework.response import Response

from trashcans.models import Trashcan
from trashcans.serializers import TrashcanSerializer
from rest_framework import viewsets, status


class TrashcanViewSet(viewsets.ModelViewSet):
    queryset = Trashcan.objects.all()
    serializer_class = TrashcanSerializer


@api_view(['GET'])
def get_trashcan_csv(request):
    # Trashcan.objects.all().delete()

    CSV_PATH = 'static/seoul_trashcan.csv'

    with open(CSV_PATH, newline='') as csvfile:
        data_reader = csv.DictReader(csvfile)

        for row in data_reader:
            Trashcan.objects.create(
                address=row['road_name'],
                latitude=row['lat'],
                longitude=row['long'],
                # longitude=round(float(row['long']), 3),   # 소수점 반올림 필요하다면?
                state='C'
            )
    return Response(status=status.HTTP_200_OK)
