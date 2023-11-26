from datetime import datetime
from time import mktime

from celery import Celery
from django.core.cache import cache

from core.models import DataSource, Episode, Provider
from core.shared import CommonResponse
from spreaker.services import get_audio, get_rss_data, get_rssurl

app = Celery("tasks")


@app.task
def download_episode_sk(episode_id) -> CommonResponse:
    out = CommonResponse()
    try:
        episode = Episode.objects.get(episode_id=episode_id)
        download = get_audio(input_url=episode.target, fname="sk_%s" % episode_id)
        episode.is_downloaded = True
        episode.save()
        out.message = download.message
        out.status = download.status
    except Episode.DoesNotExist:
        out.message = "Episode ID not found"
        out.status = "error"
    return out.__dict__


@app.task
def import_episodes_sk() -> CommonResponse:
    out = CommonResponse()
    try:
        provider = Provider.objects.get(name="Spreaker")
        datasource = DataSource.objects.filter(provider=provider)
        for podcast in datasource:
            datasource_obj = DataSource.objects.get(id=podcast.id)
            rss_feed_url = get_rssurl(datasource_obj.target)
            if rss_feed_url.status == "success":
                rss_feed = get_rss_data(rss_feed_url.value).value
                for feed in rss_feed:
                    id = feed["id"].split("/")[-1]
                    check_episode = Episode.objects.filter(episode_id=id, datasource=datasource_obj)
                    if not check_episode:
                        try:
                            target_link = feed["links"][1]["href"]
                        except IndexError:
                            target_link = feed["links"][0]["href"]
                        Episode.objects.create(
                            episode_id=id,
                            name=feed["title"],
                            datasource=datasource_obj,
                            episode_date=datetime.fromtimestamp(mktime(feed["published_parsed"])),
                            target=target_link,
                        )
                        cache.clear()
                out.message = "done"
                out.status = "success"
            else:
                out.message = "Feed Rss issue."
                out.status = "error"
    except Provider.DoesNotExist:
        out.status = "error"
        out.message = "Spreaker provider not exists"
    return out.__dict__
