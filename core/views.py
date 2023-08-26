from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from core.models import DataSource, Episode, Playlist


# Create your views here.
class HomepageView(LoginRequiredMixin, View):
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


class PlayerView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "core/player.html")
