from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import resolve, reverse
from django.utils import timezone
from rest_framework.test import APIClient

from core.models import DataSource, Episode, Playlist, Provider


# Create your tests here.
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

    def test_urls(self):
        self.assertEqual(reverse("api:playlist"), "/api/playlist/")
        self.assertEqual(resolve("/api/playlist/").view_name, "api:playlist")

    def test_view(self):
        client = APIClient()
        response = client.get("/api/playlist/")
        self.assertEqual(response.json(), {"detail": "Authentication credentials were not provided."})
        client.login(username="testuser", password="1234", headers={"Content-Type": "application/json"})
        response = client.get("/api/playlist/")
        self.assertEqual(response.json()[0]["episode"]["name"], "Introducing the shorter side of YouTube")
        response = client.get("/api/episode/")
        self.assertEqual(response.json()[0]["name"], "Introducing the shorter side of YouTube")
        response = client.post("/api/playlist/edit/yt/xxxx/", {})
        self.assertEqual(response.json(), {"status": "error", "message": "Episode not found.", "value": None})
        response = client.post("/api/playlist/edit/xyz/__NeP0RqACU/", {})
        self.assertEqual(response.json(), {"status": "error", "message": "Provider not found.", "value": None})
        response = client.post("/api/playlist/edit/ytc/__NeP0RqACU/", {})
        self.assertEqual(response.json(), {"status": "error", "message": "Datasource not found.", "value": None})
        response = client.post("/api/playlist/edit/yt/__NeP0RqACU/", {})
        self.assertEqual(response.json(), {"status": "success", "message": "Already in the playlist.", "value": None})
        response = client.post("/api/playlist/edit/yt/thA_T13Wnqo/", {})
        self.assertEqual(response.json(), {"message": None, "status": "success", "value": None})


class Models_TestCase(TestCase):
    def setUp(self):
        Provider.objects.create(name="Youtube", icon="aaaa", color="#fff")
        provider = Provider.objects.get(name="Youtube")
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

    def test_str(self):
        provider = Provider.objects.get(name="Youtube")
        self.assertEqual(str(provider), "Youtube")
        datasource = DataSource.objects.get(name="Youtube Official Channel")
        self.assertEqual(str(datasource), "Youtube/Youtube Official Channel")
        episode = Episode.objects.get(name="Introducing the shorter side of YouTube")
        self.assertEqual(str(episode), "Youtube/Youtube Official Channel/Introducing the shorter side of YouTube")
        playlist = Playlist.objects.get(order_num=1)
        self.assertEqual(str(playlist), "Introducing the shorter side of YouTube")

    def test_homepage(self):
        client = Client()
        response = client.get("/")
        self.assertEqual(response.status_code, 302)
        client.login(username="testuser", password="1234")
        response_logged = client.get("/")
        self.assertEqual(response_logged.status_code, 200)
        client.logout()

    def test_player(self):
        client = Client()
        response = client.get("/player/")
        self.assertEqual(response.status_code, 302)
        client.login(username="testuser", password="1234")
        response_logged = client.get("/player/")
        self.assertEqual(response_logged.status_code, 200)
        client.logout()
