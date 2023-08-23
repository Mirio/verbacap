from django.db.models import Max
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from core.api.serializers import EpisodeSerializer, PlaylistSerializer
from core.models import DataSource, Episode, Playlist, Provider
from core.services import download_episode
from core.shared import CommonResponse


class PlaylistView(APIView):
    def get(self, request, format=None):
        playlist = Playlist.objects.all()
        serializer = PlaylistSerializer(playlist, many=True)
        return Response(serializer.data)


class PlaylistEditView(APIView):
    def post(self, request, provider_shortname, episode_id, format=None):
        out = CommonResponse()
        try:
            provider = Provider.objects.get(shortname=provider_shortname)
            datasource = DataSource.objects.get(provider=provider)
            episode = Episode.objects.get(datasource=datasource, episode_id=episode_id)
            try:
                Playlist.objects.get(episode=episode)
                out.status = "success"
                out.message = "Already in the playlist."
            except Playlist.DoesNotExist:
                ordernum_max = Playlist.objects.aggregate(Max("order_num"))["order_num__max"]
                download_episode(provider_shortname=provider.shortname, episode_id=episode.episode_id)
                obj = Playlist(order_num=ordernum_max + 1, episode=episode)
                obj.save()
                out.status = "success"
        except Provider.DoesNotExist:
            out.status = "error"
            out.message = "Provider not found."
        except Episode.DoesNotExist:
            out.status = "error"
            out.message = "Episode not found."
        except DataSource.DoesNotExist:
            out.status = "error"
            out.message = "Datasource not found."
        return Response(out.__dict__)


class EpisodeSerializerViewSet(ListModelMixin, GenericViewSet):
    serializer_class = EpisodeSerializer
    queryset = Episode.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["episode_id"]
