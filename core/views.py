from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page

from core.models import DataSource, Episode, Playlist, Settings


# Create your views here.
@method_decorator([login_required, cache_page(settings.CACHE_DEFAULT_TTL)], name="dispatch")
class Core_HomepageView(View):
    def get(self, request):
        episode = Episode.objects.all().order_by("-episode_date")
        playlist = Playlist.objects.all()
        episode_extended = []
        for iter_episode in episode:
            episodeobj = iter_episode
            for iter_playlist in playlist:
                if iter_episode.target == iter_playlist.episode.target:
                    episodeobj.is_playlist_present = True
            episode_extended.append(episodeobj)
        context = {
            "stat": {
                "total_followed": DataSource.objects.count(),
                "total_episode": episode.count(),
                "total_episode_viewed": episode.filter(is_viewed=True).count(),
            },
            "episodes": episode_extended[0:25],
            "playlist": playlist[0:25],
        }
        return render(request, "core/index.html", context=context)


@method_decorator([login_required, cache_page(settings.CACHE_DEFAULT_TTL)], name="dispatch")
class Core_PlayerView(View):
    def get(self, request):
        return render(request, "core/player.html")


class Core_HealthView(View):
    def get(self, request):
        # TODO: Implement a more deeper health check
        return HttpResponse("ok")


@method_decorator([login_required, cache_page(settings.CACHE_DEFAULT_TTL)], name="dispatch")
class Core_AddDataSourceView(View):
    def get(self, request):
        return render(request, "core/add_datasource.html")


@method_decorator([login_required, cache_page(settings.CACHE_DEFAULT_TTL)], name="dispatch")
class Core_DeleteDataSourceView(View):
    def get(self, request):
        return render(request, "core/delete_datasource.html")


@method_decorator([login_required, cache_page(settings.CACHE_DEFAULT_TTL)], name="dispatch")
class Core_Settings(View):
    def get(self, request):
        try:
            total_size = Settings.objects.get(name="persist_total_size")
        except Settings.DoesNotExist:
            total_size = 0
        try:
            total_count = Settings.objects.get(name="persist_total_count")
        except Settings.DoesNotExist:
            total_count = 0
        return render(request, "core/settings.html", context={"total_size": total_size, "total_count": total_count})


@method_decorator([login_required, cache_page(settings.CACHE_SMART_TTL)], name="dispatch")
class Core_EpisodeView(View):
    def get(self, request):
        episode_extended = []
        playlist = Playlist.objects.all()
        for iter_episode in Episode.objects.all().order_by("-episode_date"):
            episodeobj = iter_episode
            for iter_playlist in playlist:
                if iter_episode.target == iter_playlist.episode.target:
                    episodeobj.is_playlist_present = True
            episode_extended.append(episodeobj)
        return render(request, "core/episode.html", context={"episodes": episode_extended})


@method_decorator([login_required, cache_page(settings.CACHE_SMART_TTL)], name="dispatch")
class Core_PlaylistView(View):
    def get(self, request):
        playlist = Playlist.objects.all()
        return render(request, "core/playlist.html", context={"playlist": playlist})
