from datetime import datetime
from time import mktime

from celery import Celery

from core.models import DataSource, Episode, Provider
from core.services import CommonResponse
from youtube.services import get_rss, get_rssurl

app = Celery("tasks")


@app.task
def import_episodes() -> None:
    out = CommonResponse()
    try:
        youtubeprovider = Provider.objects.get(name="Youtube")
        datasource = DataSource.objects.filter(provider=youtubeprovider)
        for channels in datasource:
            datasource_obj = DataSource.objects.get(id=channels.id)
            rss_url = get_rssurl(channels.target).value
            rss_feed = get_rss(rss_url).value
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
            out.message = "Done"
            out.status = "Success"
    except Provider.DoesNotExist:
        out.status = "error"
        out.message = "Youtube provider not exists"
    return out
