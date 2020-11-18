from quests.models import Quest
from quests.serializers import QuestSerializer
from rest_framework import viewsets


class QuestViewSet(viewsets.ModelViewSet):
    queryset = Quest.objects.all()
    serializer_class = QuestSerializer
    http_method_names = ['get', 'head']
