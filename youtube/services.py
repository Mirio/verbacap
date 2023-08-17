import feedparser
import requests
from bs4 import BeautifulSoup
from django.conf import settings
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

from core.services import CommonResponse


def get_rssurl(input_url: str) -> CommonResponse:
    out = CommonResponse()
    if not input_url.startswith("https://www.youtube.com/"):
        out.status = "error"
        out.message = "Not a youtube url"
    else:
        req = requests.get(url=input_url, cookies={"CONSENT": "YES+"})
        soup = BeautifulSoup(req.text, features="html.parser")
        for iter in soup.findAll("link"):
            if "type" in iter.attrs.keys():
                if iter.attrs["type"] == "application/rss+xml":
                    out.status = "success"
                    out.value = iter.attrs["href"]
    return out


def get_rss(input_url: str, limit: int = 10) -> CommonResponse:
    out = CommonResponse()
    counter = 0
    if not input_url.startswith("https://www.youtube.com/"):
        out.status = "error"
        out.message = "Not a youtube url"
    else:
        req = feedparser.parse(url_file_stream_or_string=input_url)
        out.value = []
        for iter in req["entries"]:
            if counter == limit:
                break
            out.value.append(iter)
            counter += 1
    return out


def get_audio(input_url: str, fname: str) -> CommonResponse:
    out = CommonResponse()
    if not input_url.startswith("https://www.youtube.com/"):
        out.status = "error"
        out.message = "Not a youtube url"
    else:
        ytdl = YoutubeDL(
            params={
                "format": "bestaudio",
                "quiet": True,
                "paths": {"home": settings.PERSIST_AUDIO_ROOTDIR},
                "outtmpl": "%s" % fname,
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                    }
                ],
            }
        )
        try:
            ytdl.download(url_list=[input_url])
        except DownloadError:
            out.status = "error"
            out.message = "Some errors found during downloading."
    return out
