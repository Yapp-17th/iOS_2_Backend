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

    # def create(self, request, *args, **kwargs):
        # 쓰레기통 추가할 떄 더 설정을 해줘야 했었던거 같은데,,
        # Trashcan.objects.create(latitude=request.data["latitude"], longitude=request.data["longitude"])

    def destroy(self, request, *args, **kwargs):
        '''
                지정한 쓰레기통에 대해 삭제 요청을 보내는 API
                ---
                (토큰 필요X)
                삭제 요청이 오면 delete_cnt 값이 증가하며, delete_cnt 값이 3이 되면 삭제한다.
        '''
        instance = self.get_object()
        instance.delete_cnt += 1
        instance.save()
        if instance.delete_cnt == 3:
            self.perform_destroy(instance)
        return Response(self.get_serializer(instance).data)


@api_view(['GET'])
def get_trashcan_csv(request):
    '''
            csv 파일의 쓰레기통 정보를 가져옴
            ---
            (토큰 필요X)
    '''
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
