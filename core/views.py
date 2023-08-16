from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from core.models import DataSource, Episode, Playlist


# Create your views here.
class HomepageView(LoginRequiredMixin, View):
    def get(self, request):
        episode = Episode.objects.all()
        context = {
            "stat": {
                "total_followed": DataSource.objects.count(),
                "total_episode": episode.count(),
                "total_episode_viewed": episode.filter(is_viewed=True).count(),
            },
            "episodes": Episode.objects.all(),
            "playlist": Playlist.objects.all()[0:10],
        }
        return render(request, "core/index.html", context=context)


class PlayerView(LoginRequiredMixin, View):
    def get(self, request):
        context = {"playlist": Playlist.objects.all()}
        return render(request, "core/player.html", context=context)
