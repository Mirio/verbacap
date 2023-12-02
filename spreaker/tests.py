from os import remove
from os.path import exists

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from core.models import DataSource, Episode, Playlist, Provider
from spreaker.services import get_audio, get_rss_data, get_rssurl
from spreaker.tasks import download_episode_sk, import_episodes_sk


# Create your tests here.
class Services_TestCase(TestCase):
    def test_get_rssurl(self):
        valid = get_rssurl("https://www.spreaker.com/show/tracce-di-luca-mazzucchelli-psicologia")
        self.assertEqual(
            valid.__dict__,
            {"status": "success", "message": None, "value": "https://www.spreaker.com/show/1238441/episodes/feed"},
        )
        invalidfullurl = get_rssurl("https://www.spreaker.com/show/nonexist")
        self.assertEqual(
            invalidfullurl.__dict__, {"status": "error", "message": "Error getting feed url", "value": None}
        )
        invalidurl = get_rssurl("https://www.spreaker.it")
        self.assertEqual(invalidurl.__dict__, {"status": "error", "message": "Not a spreaker url", "value": None})

    def test_get_rss_data(self):
        valid = get_rss_data("https://www.spreaker.com/show/1238441/episodes/feed")
        self.assertEqual(valid.value[0]["title_detail"]["language"], None)
        invalidurl = get_rss_data("https://www.spreaker.it")
        self.assertEqual(invalidurl.__dict__, {"status": "error", "message": "Not a spreaker url", "value": None})

    def test_get_audio(self):
        valid = get_audio(
            "https://dts.podtrac.com/redirect.mp3/api.spreaker.com/download/episode/56960182/"
            "come_scegliere_il_lavoro_che_fa_per_te_cosa_faresti_se_avessi_9_vite_audio_extractor_net.mp3",
            "sk_56960182",
        )
        self.assertEqual(valid.__dict__, {"status": "success", "message": "Downloaded.", "value": None})
        downloaded = get_audio(
            "https://dts.podtrac.com/redirect.mp3/api.spreaker.com/download/episode/56960182/"
            "come_scegliere_il_lavoro_che_fa_per_te_cosa_faresti_se_avessi_9_vite_audio_extractor_net.mp3",
            "sk_56960182",
        )
        self.assertEqual(downloaded.__dict__, {"status": "success", "message": "Already downloaded.", "value": None})
        invalid = get_audio("https://example.com", "sk_a")
        self.assertEqual(invalid.__dict__, {"status": "error", "message": "Not a spreaker url", "value": None})

    def tearDown(self) -> None:
        files_todelete = ["/tmp/sk_56960182.mp3"]
        for fname in files_todelete:
            if exists(fname):
                remove(fname)


class Views_TestCase(TestCase):
    def setUp(self):
        Provider.objects.create(name="Spreaker", icon="aaaa", color="#fff")
        provider = Provider.objects.get(name="Spreaker")
        DataSource.objects.create(
            name="Psicologia con Luca Mazzucchelli",
            provider=provider,
            target="https://www.spreaker.com/show/tracce-di-luca-mazzucchelli-psicologia",
        )
        datasource = DataSource.objects.get(name="Psicologia con Luca Mazzucchelli")
        Episode.objects.create(
            name="Come scegliere il lavoro che fa per te: cosa faresti se avessi 9 vite?",
            datasource=datasource,
            episode_id="1",
            episode_date=timezone.now(),
            target=(
                "https://api.spreaker.com/download/episode/56960182/come_scegliere_il_lavoro_"
                "che_fa_per_te_cosa_faresti_se_avessi_9_vite_audio_extractor_net.mp3"
            ),
        )
        episode = Episode.objects.get(name="Come scegliere il lavoro che fa per te: cosa faresti se avessi 9 vite?")
        Playlist.objects.create(episode=episode, order_num=1)
        user = get_user_model().objects.create_user("testuser")
        user.set_password("1234")
        user.save()

    def tearDown(self) -> None:
        files_todelete = ["/tmp/sk_1.mp3"]
        for fname in files_todelete:
            if exists(fname):
                remove(fname)

    def test_adddatasourceview(self):
        client = Client()
        response = client.get("/sk/add-podcast/")
        self.assertEqual(response.status_code, 302)
        client.login(username="testuser", password="1234")
        response_logged = client.get("/sk/add-podcast/")
        self.assertEqual(response_logged.status_code, 200)
        response_post = client.post(
            "/sk/add-podcast/",
            {"name": "aaaa", "podcast_url": "https://www.spreaker.com/show/tracce-di-luca-mazzucchelli-psicologia"},
        )
        self.assertEqual(response_post.status_code, 422)
        response_post = client.post("/sk/add-podcast/", {"name": "aaaa", "podcast_url": "https://www.youtube.it"})
        self.assertEqual(response_post.status_code, 400)
        response_post = client.post("/sk/add-podcast/", {"name": "aaaa"})
        self.assertEqual(response_post.status_code, 400)

    def test_removedatasourceview(self):
        provider = Provider.objects.get(name="Spreaker")
        client = Client()
        response = client.get("/sk/delete-podcast/")
        self.assertEqual(response.status_code, 302)
        client.login(username="testuser", password="1234")
        response_logged = client.get("/sk/delete-podcast/")
        self.assertEqual(response_logged.status_code, 200)
        obj = DataSource.objects.get(provider=provider, name="Psicologia con Luca Mazzucchelli")
        response_post = client.post("/sk/delete-podcast/", {"datasource_id": obj.pk})
        self.assertEqual(response_post.status_code, 200)
        response_post = client.post("/sk/delete-podcast/", {"datasource_id": obj.pk})
        self.assertEqual(response_post.status_code, 404)
        response_post = client.post("/sk/delete-podcast/", {"aaa": "foo"})
        self.assertEqual(response_post.status_code, 400)

    def test_import_episodes_sk(self):
        obj = import_episodes_sk()
        self.assertEqual(obj, {"status": "success", "message": "done", "value": None})

    def test_download_episode_sk(self):
        obj = download_episode_sk(episode_id="1")
        self.assertEqual(obj, {"message": "Downloaded.", "status": "success", "value": None})
        obj_noexist = download_episode_sk(episode_id="xyz")
        self.assertEqual(obj_noexist, {"message": "Episode ID not found", "status": "error", "value": None})


class ApiUrl_Test(TestCase):
    def setUp(self):
        Provider.objects.create(name="Youtube", icon="aaaa", color="#fff", shortname="yt")
        provider = Provider.objects.get(name="Youtube")
        Provider.objects.create(name="Youtube-Custom", icon="aaaa", color="#fff", shortname="ytc")
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
            episode_id="__NeP0RqACU",
            is_downloaded=True,
            target="https://www.youtube.com/watch?v=__NeP0RqACU",
        )
        Episode.objects.create(
            name="Celebrating The Mario Community & 100 BILLION Views",
            datasource=datasource,
            episode_date=timezone.now(),
            episode_id="thA_T13Wnqo",
            target="https://www.youtube.com/watch?v=thA_T13Wnqo",
        )
        episode = Episode.objects.get(name="Introducing the shorter side of YouTube")
        Playlist.objects.create(episode=episode, order_num=1)
        user = get_user_model().objects.create_user("testuser")
        user.set_password("1234")
        user.save()

    def test_actions(self):
        client = APIClient()
        client.login(username="testuser", password="1234", headers={"Content-Type": "application/json"})
        response = client.put(reverse("api:api-task-sk-importepisodes"))
        self.assertEqual(response.json(), {"success": True})
