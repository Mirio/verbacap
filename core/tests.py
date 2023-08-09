from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from core.models import DataSource, Episode, Playlist, Provider

# Create your tests here.


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
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
        self.client.login(username="testuser", password="1234")
        response_logged = self.client.get("/")
        self.assertEqual(response_logged.status_code, 200)
