from os.path import exists

from django.test import TestCase
from django.utils import timezone

from core.models import DataSource, Episode, Provider
from youtube.services import get_audio, get_rss, get_rssurl
from youtube.tasks import download_episode_yt, import_episodes_yt


# Create your tests here.
class Services_TestCase(TestCase):
    def setUp(self):
        Provider.objects.create(name="Youtube", icon="aaaa", color="#fff", shortname="yt")
        provider = Provider.objects.get(name="Youtube")
        DataSource.objects.create(
            name="Youtube Official Channel",
            provider=provider,
            target="https://www.youtube.com/@YouTube",
        )
        datasource = DataSource.objects.get(name="Youtube Official Channel")
        Episode.objects.create(
            name="Introducing the shorter side of YouTube",
            datasource=datasource,
            episode_date=timezone.now(),
            episode_id="__NeP0RqACU",
            target="https://www.youtube.com/watch?v=__NeP0RqACU",
        )

    def test_get_rssurl(self):
        rssurl = get_rssurl("https://www.youtube.com/@YouTube")
        self.assertEqual(
            rssurl.__dict__,
            {
                "message": None,
                "status": "success",
                "value": "https://www.youtube.com/feeds/videos.xml?channel_id=UCBR8-60-B28hp2BmDPdntcQ",
            },
        )
        rssurl_noexists = get_rssurl("https://example.com")
        self.assertEqual(rssurl_noexists.__dict__, {"status": "error", "message": "Not a youtube url", "value": None})

    def test_get_rss(self):
        rssurl = get_rssurl("https://www.youtube.com/@YouTube")
        self.assertEqual(type(get_rss(rssurl.value).value), list)
        rssurl_noexists = get_rss(input_url="https://example.com")
        self.assertEqual(rssurl_noexists.__dict__, {"status": "error", "message": "Not a youtube url", "value": None})
        rssurl_missing = get_rss(input_url="")
        self.assertEqual(rssurl_missing.__dict__, {"status": "error", "message": "Input url missing", "value": None})

    def test_get_audio(self):
        getaudio = get_audio("https://www.youtube.com/watch?v=npFE7NIy574", fname="a")
        self.assertEqual(exists("/tmp/a.mp3"), True)
        self.assertEqual(getaudio.__dict__, {"status": "success", "message": "Downloaded.", "value": None})
        getaudio = get_audio("https://www.youtube.com/watch?v=npFE7NIy574", fname="a")
        self.assertEqual(getaudio.__dict__, {"status": "success", "message": "Already downloaded.", "value": None})
        download_audio_noyt = get_audio("https://example.com", "a")
        self.assertEqual(
            download_audio_noyt.__dict__, {"message": "Not a youtube url", "status": "error", "value": None}
        )
        download_audio_error = get_audio("https://www.youtube.com/watch?v=noexists", fname="b")
        self.assertEqual(
            download_audio_error.__dict__,
            {"message": "Some errors found during downloading.", "status": "error", "value": None},
        )

    def test_import_episodes(self):
        obj = import_episodes_yt()
        self.assertEqual(obj.__dict__, {"status": "success", "message": "done", "value": None})

    def test_download_episode_yt(self):
        obj = download_episode_yt(episode_id="__NeP0RqACU")
        self.assertEqual(obj, {"message": "Downloaded.", "status": "success", "value": None})
        obj_noexist = download_episode_yt(episode_id="xyz")
        self.assertEqual(obj_noexist, {"message": "Episode ID not found", "status": "error", "value": None})
