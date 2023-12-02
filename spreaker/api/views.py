from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.serializers import CommonSuccessSerializer
from spreaker.tasks import import_episodes_sk


class Task_SK_ImportEpisodeSK(APIView):
    serializer_class = None

    def put(self, request, format=None):
        obj = import_episodes_sk.delay()
        out = obj.id
        serializer = CommonSuccessSerializer({"success": out})
        return Response(serializer.data)
