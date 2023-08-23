from datetime import datetime
from time import mktime

from celery import Celery

from core.models import DataSource, Episode, Provider
from core.shared import CommonResponse
from youtube.services import get_audio, get_rss, get_rssurl

app = Celery("tasks")


@app.task
def download_episode_yt(episode_id) -> CommonResponse:
    out = CommonResponse()
    try:
        episode = Episode.objects.get(episode_id=episode_id)
        download = get_audio(input_url=episode.target, fname=episode_id)
        out.message = download.message
        out.status = download.status
    except Episode.DoesNotExist:
        out.message = "Episode ID not found"
        out.status = "error"
    return out.__dict__


@app.task
def import_episodes_yt() -> CommonResponse:
    out = CommonResponse()
    try:
        youtubeprovider = Provider.objects.get(name="Youtube")
        datasource = DataSource.objects.filter(provider=youtubeprovider)
        for channels in datasource:
            datasource_obj = DataSource.objects.get(id=channels.id)
            rss_url = get_rssurl(channels.target)
            if rss_url.status == "success":
                rss_feed = get_rss(rss_url.value).value
                for feed in rss_feed:
                    check_episode = Episode.objects.filter(episode_id=feed["yt_videoid"])
                    if not check_episode:
                        obj = Episode(
                            episode_id=feed["yt_videoid"],
                            name=feed["title"],
                            datasource=datasource_obj,
                            episode_date=datetime.fromtimestamp(mktime(feed["published_parsed"])),
                            target=feed["link"],
                        )
                        obj.save()
                out.message = "done"
                out.status = "success"
            else:
                out.message = "Feed Rss issue."
                out.status = "error"
    except Provider.DoesNotExist:
        out.status = "error"
        out.message = "Youtube provider not exists"
    return out
