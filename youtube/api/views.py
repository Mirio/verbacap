from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.serializers import CommonSuccessSerializer
from youtube.tasks import import_episodes_yt_channels, import_episodes_yt_playlist


class Task_YT_ImportEpisodesYTChannel(APIView):
    serializer_class = None

    def put(self, request, format=None):
        obj = import_episodes_yt_channels.delay()
        out = obj.id
        serializer = CommonSuccessSerializer({"success": out})
        return Response(serializer.data)


class Task_YT_ImportEpisodesYTPlaylist(APIView):
    serializer_class = None

    def put(self, request, format=None):
        obj = import_episodes_yt_playlist.delay()
        out = obj.id
        serializer = CommonSuccessSerializer({"success": out})
        return Response(serializer.data)
