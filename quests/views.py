from quests.models import Quest
from quests.serializers import QuestSerializer
from rest_framework import viewsets


class QuestViewSet(viewsets.ModelViewSet):
    queryset = Quest.objects.all()
    serializer_class = QuestSerializer
    # 퀘스트는 CRUD 필요없음
    http_method_names = []
