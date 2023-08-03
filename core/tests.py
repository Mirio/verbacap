from django.test import TestCase
from django.utils import timezone

from core.models import DataSource, Episode, Provider

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

    def test_str(self):
        provider = Provider.objects.get(name="Youtube")
        self.assertEqual(str(provider), "Youtube")
        datasource = DataSource.objects.get(name="Youtube Official Channel")
        self.assertEqual(str(datasource), "Youtube/Youtube Official Channel")
        episode = Episode.objects.get(name="Introducing the shorter side of YouTube")
        self.assertEqual(str(episode), "Youtube/Youtube Official Channel/Introducing the shorter side of YouTube")
