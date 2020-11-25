import csv

from rest_framework.decorators import api_view
from rest_framework.response import Response

from trashcans.models import Trashcan
from trashcans.serializers import TrashcanSerializer
from rest_framework import viewsets, status


class TrashcanViewSet(viewsets.ModelViewSet):
    queryset = Trashcan.objects.all()
    serializer_class = TrashcanSerializer
    http_method_names = ['get', 'post', 'delete', 'head']

    def create(self, request, *args, **kwargs):
        '''
                쓰레기통 추가
                ---
                (토큰 필요)
                위도, 경도, 주소명으로 쓰레기통 추가
        '''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        '''
                쓰레기통 삭제
                ---
                (토큰 필요)
                삭제 요청이 오면 delete_cnt 값이 증가하며, delete_cnt 값이 3이 되면 삭제한다.
        '''
        instance = self.get_object()
        instance.delete_cnt += 1
        instance.save()
        if instance.delete_cnt == 3:
            self.perform_destroy(instance)
        return Response(self.get_serializer(instance).data)


# @api_view(['GET'])
# def get_trashcan_csv(request):
#     '''
#             csv 파일의 쓰레기통 정보를 가져옴
#             ---
#             (토큰 필요X)
#     '''
#     Trashcan.objects.all().delete()
#
#     CSV_PATH = 'static/seoul_trashcan.csv'
#
#     with open(CSV_PATH, newline='') as csvfile:
#         data_reader = csv.DictReader(csvfile)
#
#         for row in data_reader:
#             Trashcan.objects.create(
#                 address=row['road_name'],
#                 latitude=row['lat'],
#                 longitude=row['long'],
#                 # longitude=round(float(row['long']), 3),   # 소수점 반올림 필요하다면?
#                 state='C'
#             )
#     return Response(status=status.HTTP_200_OK)
