from django.core.cache import cache
from django.db.models import Max
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from core.api.serializers import CommonSuccessSerializer, EpisodeSerializer, PlaylistSerializer
from core.models import DataSource, Episode, Playlist, Provider
from core.services import download_episode
from core.shared import CommonResponse
from core.tasks import calcolate_persistinfo


class Action_AppCacheCleanupView(APIView):
    serializer_class = None

    def delete(self, request, format=None):
        serializer = CommonSuccessSerializer({"success": bool(cache.clear())})
        return Response(serializer.data)


class Task_CoreCalcolatePersistInfoView(APIView):
    serializer_class = None

    def put(self, request, format=None):
        obj = calcolate_persistinfo.delay()
        out = obj.id
        serializer = CommonSuccessSerializer({"success": out})
        return Response(serializer.data)


class UpdatePlayerTimeView(APIView):
    serializer_class = None

    def put(self, request, provider_shortname, episode_id, current_time, format=None):
        cache_key = f"UpdatePlayerTime_{provider_shortname}_{episode_id}"
        cache.set(cache_key, current_time)
        return Response()


class PlaylistView(APIView):
    serializer_class = PlaylistSerializer

    def get(self, request, format=None):
        playlist = []
        for iter in Playlist.objects.all().order_by("order_num"):
            if iter.episode.is_downloaded:
                current_time = cache.get(
                    "UpdatePlayerTime_{}_{}".format(
                        iter.episode.datasource.provider.shortname, iter.episode.episode_id
                    )
                )
                if current_time:
                    iter.episode.current_time = current_time
                playlist.append(iter)
        serializer = PlaylistSerializer(playlist, many=True)
        return Response(serializer.data)


class PlaylistEditView(APIView):
    serializer_class = None

    def delete(self, request, provider_shortname, episode_id, format=None):
        out = CommonResponse()
        try:
            provider = Provider.objects.get(shortname=provider_shortname)
            datasource = DataSource.objects.get(provider=provider)
            episode = Episode.objects.get(datasource=datasource, episode_id=episode_id)
            try:
                obj = Playlist.objects.get(episode=episode)
                obj.delete()
                out.status = "success"
                out.message = "Delete from playlist."
            except Playlist.DoesNotExist:
                out.status = "done"
                out.message = "The episode is not in the playlist."
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

    def put(self, request, provider_shortname, episode_id, format=None):
        out = CommonResponse()
        episode = None
        try:
            provider = Provider.objects.get(shortname=provider_shortname)
            episodes = Episode.objects.filter(episode_id=episode_id)
            for iter in episodes.all():
                if iter.datasource.provider.shortname == provider_shortname:
                    episode = iter
                    break
            if episode:
                try:
                    Playlist.objects.get(episode=episode)
                    out.status = "success"
                    out.message = "Already in the playlist."
                except Playlist.DoesNotExist:
                    ordernum_max = Playlist.objects.aggregate(Max("order_num"))["order_num__max"]
                    if not ordernum_max:
                        ordernum_max = 0
                    download_episode(provider_shortname=provider.shortname, episode_id=episode.episode_id)
                    obj = Playlist(order_num=ordernum_max + 1, episode=episode)
                    obj.save()
                    out.status = "success"
            else:
                out.message = "Episode not found."
                out.status = "error"
        except Provider.DoesNotExist:
            out.status = "error"
            out.message = "Provider not found."
        return Response(out.__dict__)


class EpisodeViewedView(APIView):
    serializer_class = None

    def put(self, request, provider_shortname, episode_id, format=None):
        out = CommonResponse()
        episode_exists = False
        try:
            provider = Provider.objects.get(shortname=provider_shortname)
            datasources = DataSource.objects.filter(provider=provider)
            if not datasources:
                raise DataSource.DoesNotExist
            for datasource in datasources:
                try:
                    episode = Episode.objects.get(datasource=datasource, episode_id=episode_id)
                    episode_exists = True
                    break
                except Episode.DoesNotExist:
                    pass
            if not episode_exists:
                raise Episode.DoesNotExist
            playlist = Playlist.objects.get(episode=episode)
            if not episode.is_viewed:
                episode.is_viewed = True
                episode.save()
            playlist.delete()
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
