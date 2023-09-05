from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from core.models import DataSource, Provider
from youtube.forms import AddChannelForm


# Create your views here.
class AddChannelView(LoginRequiredMixin, View):
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


class DeleteChannelView(LoginRequiredMixin, View):
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
