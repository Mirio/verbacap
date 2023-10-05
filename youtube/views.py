from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import render
from django.views import View

from core.models import DataSource, Provider
from youtube.forms import AddChannelForm, AddPlaylistForm
from youtube.tasks import import_episodes_yt_channels, import_episodes_yt_playlist


# Create your views here.
class Youtube_AddPlaylistView(LoginRequiredMixin, View):
    def get(self, request):
        form = AddPlaylistForm()
        return render(request, "youtube/add-playlist.html", context={"form": form})

    def post(self, request):
        form = AddPlaylistForm(request.POST)
        outmsg = None
        status = 200
        if form.is_valid():
            target = form.cleaned_data["playlist_url"]
            name = form.cleaned_data["name"]
            if "&list=" in target:
                provider = Provider.objects.get(name="Youtube-Playlist")
                match = DataSource.objects.filter(provider=provider, target=target)
                if not match:
                    DataSource.objects.create(provider=provider, target=target, name=name)
                    outmsg = "Added."
                    transaction.on_commit(import_episodes_yt_playlist.delay)
                else:
                    status = 422
                    outmsg = "Already present."
            else:
                status = 400
                outmsg = "Url Invalid"
            return render(
                request, "youtube/submit.html", context={"outmsg": outmsg, "back": "yt-add-playlist"}, status=status
            )
        else:
            status = 400
            outmsg = "Form invalid"
            return render(
                request, "youtube/submit.html", context={"outmsg": outmsg, "back": "yt-add-playlist"}, status=status
            )


class Youtube_DeletePlaylistView(LoginRequiredMixin, View):
    def get(self, request):
        provider = Provider.objects.get(name="Youtube-Playlist")
        return render(
            request,
            "youtube/delete-playlist.html",
            context={"datasource_obj": DataSource.objects.filter(provider=provider)},
        )

    def post(self, request):
        outmsg = None
        status = 200
        datasource_id = request.POST.get("datasource_id")
        if datasource_id:
            provider = Provider.objects.get(name="Youtube-Playlist")
            try:
                obj = DataSource.objects.get(provider=provider, pk=datasource_id)
                obj.delete()
                outmsg = "Deleted."
            except DataSource.DoesNotExist:
                outmsg = "Datasource Not Found"
                status = 404
        else:
            outmsg = "Datasource invalid"
            status = 400
        return render(request, "youtube/submit.html", context={"outmsg": outmsg}, status=status)


class Youtube_AddChannelView(LoginRequiredMixin, View):
    def get(self, request):
        form = AddChannelForm()
        return render(request, "youtube/add-channel.html", context={"form": form})

    def post(self, request):
        form = AddChannelForm(request.POST)
        outmsg = None
        status = 200
        if form.is_valid():
            target = form.cleaned_data["channel_url"]
            name = form.cleaned_data["name"]
            if target.startswith("https://www.youtube.com/@"):
                provider = Provider.objects.get(name="Youtube")
                match = DataSource.objects.filter(provider=provider, target=target.lower())
                if not match:
                    DataSource.objects.create(provider=provider, target=target.lower(), name=name)
                    outmsg = "Added."
                    transaction.on_commit(import_episodes_yt_channels.delay)
                else:
                    status = 422
                    outmsg = "Already present."
            else:
                status = 400
                outmsg = "Url Invalid"
            return render(
                request, "youtube/submit.html", context={"outmsg": outmsg, "back": "yt-add-channel"}, status=status
            )
        else:
            status = 400
            outmsg = "Form invalid"
            return render(
                request, "youtube/submit.html", context={"outmsg": outmsg, "back": "yt-add-channel"}, status=status
            )


class Youtube_DeleteChannelView(LoginRequiredMixin, View):
    def get(self, request):
        provider = Provider.objects.get(name="Youtube")
        return render(
            request,
            "youtube/delete-channel.html",
            context={"datasource_obj": DataSource.objects.filter(provider=provider)},
        )

    def post(self, request):
        outmsg = None
        status = 200
        datasource_id = request.POST.get("datasource_id")
        if datasource_id:
            provider = Provider.objects.get(name="Youtube")
            try:
                obj = DataSource.objects.get(provider=provider, pk=datasource_id)
                obj.delete()
                outmsg = "Deleted."
            except DataSource.DoesNotExist:
                outmsg = "Datasource Not Found"
                status = 404
        else:
            outmsg = "Datasource invalid"
            status = 400
        return render(request, "youtube/submit.html", context={"outmsg": outmsg}, status=status)
