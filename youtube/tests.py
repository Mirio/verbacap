from os.path import exists

from django.test import TestCase

from youtube.services import get_audio, get_rss, get_rssurl


# Create your tests here.
class Services_TestCase(TestCase):
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
        self.assertEqual(rssurl_noexists.__dict__, {"status": "error", "message": "Not a Youtube Url", "value": None})

    def test_get_rss(self):
        rssurl = get_rssurl("https://www.youtube.com/@YouTube")
        self.assertEqual(type(get_rss(rssurl.value).value), list)
        rssurl_noexists = get_rss("https://example.com")
        self.assertEqual(rssurl_noexists.__dict__, {"status": "error", "message": "Not a Youtube Url", "value": None})

    def test_get_audio(self):
        get_audio("https://www.youtube.com/watch?v=ySdna7EvUZ0", fname="a")
        self.assertEqual(exists("/tmp/a.opus"), True)
        download_audio_noyt = get_audio("https://example.com", "a")
        self.assertEqual(
            download_audio_noyt.__dict__, {"message": "Not a Youtube Url", "status": "error", "value": None}
        )
        download_audio_error = get_audio("https://www.youtube.com/watch?v=noexists", fname="b")
        self.assertEqual(
            download_audio_error.__dict__,
            {"message": "Some errors found during downloading.", "status": "error", "value": None},
        )
