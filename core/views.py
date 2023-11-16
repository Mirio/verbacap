from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from core.models import DataSource, Episode, Playlist, Settings


# Create your views here.
class Core_HomepageView(LoginRequiredMixin, View):
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


class Core_PlayerView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "core/player.html")


class Core_HealthView(View):
    def get(self, request):
        # TODO: Implement a more deeper health check
        return HttpResponse("ok")


class Core_AddDataSourceView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "core/add_datasource.html")


class Core_DeleteDataSourceView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "core/delete_datasource.html")


class Core_Settings(LoginRequiredMixin, View):
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


class Core_EpisodeView(LoginRequiredMixin, View):
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


class Core_PlaylistView(LoginRequiredMixin, View):
    def get(self, request):
        playlist = Playlist.objects.all()
        return render(request, "core/playlist.html", context={"playlist": playlist})
