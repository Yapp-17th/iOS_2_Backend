import csv

from rest_framework.decorators import api_view
from rest_framework.response import Response

from trashcans.models import Trashcan
from trashcans.serializers import TrashcanSerializer
from rest_framework import viewsets, status


class TrashcanViewSet(viewsets.ModelViewSet):
    queryset = Trashcan.objects.all()
    serializer_class = TrashcanSerializer
    http_method_names = ['get', 'post', 'delete']

    # def create(self, request, *args, **kwargs):
        # 쓰레기통 추가할 떄 더 설정을 해줘야 했었던거 같은데,,
        # Trashcan.objects.create(latitude=request.data["latitude"], longitude=request.data["longitude"])

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete_cnt += 1
        instance.save()
        if instance.delete_cnt == 3:
            self.perform_destroy(instance)
        return Response(self.get_serializer(instance).data)


@api_view(['GET'])
def get_trashcan_csv(request):
    Trashcan.objects.all().delete()

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
