from os import remove
from os.path import exists

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.utils import timezone

from core.models import DataSource, Episode, Playlist, Provider
from youtube.services import get_audio, get_channel_rssurl, get_playlist_rssurl, get_rss_data
from youtube.tasks import download_episode_yt, import_episodes_yt_channels, import_episodes_yt_playlist


# Create your tests here.
class Services_TestCase(TestCase):
    def setUp(self):
        Provider.objects.create(name="Youtube", icon="aaaa", color="#fff", shortname="yt")
        Provider.objects.create(name="Youtube-Playlist", icon="aaaa", color="#fff", shortname="yt-playlist")
        provider = Provider.objects.get(name="Youtube")
        provider_playlist = Provider.objects.get(name="Youtube-Playlist")
        DataSource.objects.create(
            name="Youtube Official Channel",
            provider=provider,
            target="https://www.youtube.com/@YouTube",
        )
        DataSource.objects.create(
            name="Youtube - Random Playlist",
            provider=provider_playlist,
            target="https://www.youtube.com/watch?v=L-PeKYY4FDY&list=PLbpi6ZahtOH5Acp2m7XRwwoi4ryCsh18P",
        )
        datasource = DataSource.objects.get(name="Youtube Official Channel")
        Episode.objects.create(
            name="Introducing the shorter side of YouTube",
            datasource=datasource,
            episode_date=timezone.now(),
            episode_id="__NeP0RqACU",
            target="https://www.youtube.com/watch?v=__NeP0RqACU",
        )

    def tearDown(self):
        files_todelete = ["/tmp/a.mp3", "/tmp/yt___NeP0RqACU.mp3"]
        for fname in files_todelete:
            if exists(fname):
                remove(fname)

    def test_get_channel_rssurl(self):
        rssurl = get_channel_rssurl("https://www.youtube.com/@YouTube")
        self.assertEqual(
            rssurl.__dict__,
            {
                "message": None,
                "status": "success",
                "value": "https://www.youtube.com/feeds/videos.xml?channel_id=UCBR8-60-B28hp2BmDPdntcQ",
            },
        )
        rssurl_noexists = get_channel_rssurl("https://example.com")
        self.assertEqual(rssurl_noexists.__dict__, {"status": "error", "message": "Not a youtube url", "value": None})

    def test_get_playlist_rssurl(self):
        rssurl = get_playlist_rssurl(
            "https://www.youtube.com/watch?v=qVxdyIsMEQo&list=PLbpi6ZahtOH7c6nDA9YG3QcyRGbZ4xDFn"
        )
        self.assertEqual(
            rssurl.__dict__,
            {
                "message": None,
                "status": "success",
                "value": "https://www.youtube.com/feeds/videos.xml?playlist_id=PLbpi6ZahtOH7c6nDA9YG3QcyRGbZ4xDFn",
            },
        )
        rssurl_noplaylist = get_playlist_rssurl("https://www.youtube.com/watch?v=qVxdyIsMEQo")
        self.assertEqual(
            rssurl_noplaylist.__dict__, {"status": "error", "message": "Not a playlist url", "value": None}
        )
        rssurl_noexists = get_channel_rssurl("https://example.com")
        self.assertEqual(rssurl_noexists.__dict__, {"status": "error", "message": "Not a youtube url", "value": None})

    def test_get_rss_data(self):
        rssurl = get_channel_rssurl("https://www.youtube.com/@YouTube")
        self.assertEqual(type(get_rss_data(rssurl.value).value), list)
        rssurl_noexists = get_rss_data(input_url="https://example.com")
        self.assertEqual(rssurl_noexists.__dict__, {"status": "error", "message": "Not a youtube url", "value": None})
        rssurl_missing = get_rss_data(input_url="")
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

    def test_import_episodes_channels(self):
        obj = import_episodes_yt_channels()
        self.assertEqual(obj, {"status": "success", "message": "done", "value": None})

    def test_import_episodes_playlist(self):
        obj = import_episodes_yt_playlist()
        self.assertEqual(obj, {"status": "success", "message": "done", "value": None})

    def test_download_episode_yt(self):
        obj = download_episode_yt(episode_id="__NeP0RqACU")
        self.assertEqual(obj, {"message": "Downloaded.", "status": "success", "value": None})
        obj_noexist = download_episode_yt(episode_id="xyz")
        self.assertEqual(obj_noexist, {"message": "Episode ID not found", "status": "error", "value": None})


class Views_TestCase(TestCase):
    def setUp(self):
        Provider.objects.create(name="Youtube", icon="aaaa", color="#fff")
        Provider.objects.create(name="Youtube-Playlist", icon="aaaa", color="#fff", shortname="yt-playlist")
        provider = Provider.objects.get(name="Youtube")
        provider_playlist = Provider.objects.get(name="Youtube-Playlist")
        DataSource.objects.create(
            name="Youtube - Random Playlist",
            provider=provider_playlist,
            target="https://www.youtube.com/watch?v=L-PeKYY4FDY&list=PLbpi6ZahtOH5Acp2m7XRwwoi4ryCsh18P",
        )
        DataSource.objects.create(
            name="Youtube Official Channel",
            provider=provider,
            target="https://www.youtube.com/feeds/videos.xml?channel_id=UCBR8-60-B28hp2BmDPdntcQ",
        )
        datasource = DataSource.objects.get(name="Youtube Official Channel")
        Episode.objects.create(
            name="Introducing the shorter side of YouTube",
            datasource=datasource,
            episode_date=timezone.now(),
            target="https://www.youtube.com/watch?v=__NeP0RqACU",
        )

        episode = Episode.objects.get(name="Introducing the shorter side of YouTube")
        Playlist.objects.create(episode=episode, order_num=1)
        user = get_user_model().objects.create_user("testuser")
        user.set_password("1234")
        user.save()

    def test_addatasourceview(self):
        client = Client()
        response = client.get("/yt/add-channel/")
        self.assertEqual(response.status_code, 302)
        client.login(username="testuser", password="1234")
        response_logged = client.get("/yt/add-channel/")
        self.assertEqual(response_logged.status_code, 200)
        response_post = client.post(
            "/yt/add-channel/", {"name": "aaaa", "channel_url": "https://www.youtube.com/@youtube"}
        )
        self.assertEqual(response_post.status_code, 200)
        response_post = client.post(
            "/yt/add-channel/", {"name": "aaaa", "channel_url": "https://www.youtube.com/@youtube"}
        )
        self.assertEqual(response_post.status_code, 422)
        response_post = client.post("/yt/add-channel/", {"name": "aaaa", "channel_url": "https://www.youtube.it"})
        self.assertEqual(response_post.status_code, 400)
        response_post = client.post("/yt/add-channel/", {"name": "aaaa"})
        self.assertEqual(response_post.status_code, 400)

        response_logged = client.get("/yt/add-playlist/")
        self.assertEqual(response_logged.status_code, 200)
        response_post = client.post(
            "/yt/add-playlist/",
            {
                "name": "aaaa",
                "playlist_url": "https://www.youtube.com/watch?v=qVxdyIsMEQo&list=PLbpi6ZahtOH7c6nDA9YG3QcyRGbZ4xDFn",
            },
        )
        self.assertEqual(response_post.status_code, 200)
        response_post = client.post(
            "/yt/add-playlist/",
            {
                "name": "aaaa",
                "playlist_url": "https://www.youtube.com/watch?v=qVxdyIsMEQo&list=PLbpi6ZahtOH7c6nDA9YG3QcyRGbZ4xDFn",
            },
        )
        self.assertEqual(response_post.status_code, 422)
        response_post = client.post("/yt/add-playlist/", {"name": "aaaa", "playlist_url": "https://www.youtube.it"})
        self.assertEqual(response_post.status_code, 400)
        response_post = client.post("/yt/add-playlist/", {"name": "aaaa"})
        self.assertEqual(response_post.status_code, 400)

    def test_deletechannelview(self):
        provider = Provider.objects.get(name="Youtube")
        provider_playlist = Provider.objects.get(name="Youtube-Playlist")
        client = Client()
        response = client.get("/yt/delete-channel/")
        self.assertEqual(response.status_code, 302)
        client.login(username="testuser", password="1234")
        response_logged = client.get("/yt/delete-channel/")
        self.assertEqual(response_logged.status_code, 200)
        obj = DataSource.objects.get(provider=provider, name="Youtube Official Channel")
        response_post = client.post("/yt/delete-channel/", {"datasource_id": obj.pk})
        self.assertEqual(response_post.status_code, 200)
        response_post = client.post("/yt/delete-channel/", {"datasource_id": obj.pk})
        self.assertEqual(response_post.status_code, 404)
        response_post = client.post("/yt/delete-channel/", {"aaa": "foo"})
        self.assertEqual(response_post.status_code, 400)
        # Playlist
        response_logged = client.get("/yt/delete-playlist/")
        self.assertEqual(response_logged.status_code, 200)
        obj = DataSource.objects.get(provider=provider_playlist, name="Youtube - Random Playlist")
        response_post = client.post("/yt/delete-playlist/", {"datasource_id": obj.pk})
        self.assertEqual(response_post.status_code, 200)
        response_post = client.post("/yt/delete-playlist/", {"datasource_id": obj.pk})
        self.assertEqual(response_post.status_code, 404)
        response_post = client.post("/yt/delete-playlist/", {"aaa": "foo"})
        self.assertEqual(response_post.status_code, 400)
