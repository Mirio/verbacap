from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page

from core.models import DataSource, Provider
from spreaker.forms import AddPodcastForm
from spreaker.tasks import import_episodes_sk


# Create your views here.
@method_decorator([login_required, cache_page(settings.CACHE_DEFAULT_TTL)], name="dispatch")
class Spreaker_AddPodcastView(View):
    def get(self, request):
        form = AddPodcastForm()
        return render(request, "spreaker/add-podcast.html", context={"form": form})

    def post(self, request):
        form = AddPodcastForm(request.POST)
        outmsg = None
        status = 200
        if form.is_valid():
            target = form.cleaned_data["podcast_url"]
            name = form.cleaned_data["name"]
            if target.startswith("https://www.spreaker.com/podcast"):
                provider = Provider.objects.get(name="Spreaker")
                match = DataSource.objects.filter(provider=provider, target=target.lower())
                if not match:
                    DataSource.objects.create(provider=provider, target=target.lower(), name=name)
                    outmsg = "Added."
                    transaction.on_commit(import_episodes_sk.delay)
                else:
                    status = 422
                    outmsg = "Already present."
            else:
                status = 400
                outmsg = "Url Invalid"
            return render(
                request, "spreaker/submit.html", context={"outmsg": outmsg, "back": "sk-add-podcast"}, status=status
            )
        else:
            status = 400
            outmsg = "Form invalid"
            return render(
                request, "spreaker/submit.html", context={"outmsg": outmsg, "back": "sk-add-channel"}, status=status
            )


@method_decorator([login_required, cache_page(settings.CACHE_DEFAULT_TTL)], name="dispatch")
class Spreaker_DeletePodcastView(View):
    def get(self, request):
        provider = Provider.objects.get(name="Spreaker")
        return render(
            request,
            "spreaker/delete-podcast.html",
            context={"datasource_obj": DataSource.objects.filter(provider=provider)},
        )

    def post(self, request):
        outmsg = None
        status = 200
        datasource_id = request.POST.get("datasource_id")
        if datasource_id:
            provider = Provider.objects.get(name="Spreaker")
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
        return render(request, "spreaker/submit.html", context={"outmsg": outmsg}, status=status)
