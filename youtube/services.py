from os.path import exists
from urllib.parse import parse_qs, urlparse

import feedparser
import requests
from bs4 import BeautifulSoup
from django.conf import settings
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

from core.shared import CommonResponse


def get_channel_rssurl(input_url: str) -> CommonResponse:
    out = CommonResponse()
    inputurl_parsed = urlparse(input_url)
    if inputurl_parsed.hostname != "www.youtube.com":
        out.status = "error"
        out.message = "Not a youtube url"
    else:
        # \/ Fake Generated SOCS, FYI "CAESE"+base64encode(msg/wrules)
        req = requests.get(
            url=input_url, cookies={"CONSENT": "PENDING+", "SOCS": "CAESEwgDEgk6NjE5NDB97TcaAml9IAEaBgiAsL-nBg"}
        )
        soup = BeautifulSoup(req.text, features="html.parser")
        for iter in soup.findAll("link"):
            if "type" in iter.attrs.keys():
                if iter.attrs["type"] == "application/rss+xml":
                    out.status = "success"
                    out.value = iter.attrs["href"]
    return out


def get_playlist_rssurl(input_url: str) -> CommonResponse:
    out = CommonResponse()
    inputurl_parsed = urlparse(input_url)
    if inputurl_parsed.hostname != "www.youtube.com":
        out.status = "error"
        out.message = "Not a youtube url"
    elif "&list=" not in input_url:
        out.status = "error"
        out.message = "Not a playlist url"
    else:
        playlist_id = parse_qs(input_url)
        out.value = "https://www.youtube.com/feeds/videos.xml?playlist_id=%s" % (playlist_id["list"][0])
        out.status = "success"
    return out


def get_rss_data(input_url: str, limit: int = 10) -> CommonResponse:
    out = CommonResponse()
    inputurl_parsed = urlparse(input_url)
    counter = 0
    if input_url:
        if inputurl_parsed.hostname != "www.youtube.com":
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
    else:
        out.status = "error"
        out.message = "Input url missing"
    return out


def get_audio(input_url: str, fname: str) -> CommonResponse:
    out = CommonResponse()
    inputurl_parsed = urlparse(input_url)
    if inputurl_parsed.hostname != "www.youtube.com":
        out.status = "error"
        out.message = "Not a youtube url"
    else:
        if not exists(f"{settings.PERSIST_AUDIO_ROOTDIR}/{fname}.mp3"):
            ytdl = YoutubeDL(
                params={
                    "format": "bestaudio",
                    "quiet": True,
                    "paths": {"home": settings.PERSIST_AUDIO_ROOTDIR},
                    "outtmpl": "%s" % fname,
                    "noprogress": True,
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
                out.status = "success"
                out.message = "Downloaded."
            except DownloadError:
                out.status = "error"
                out.message = "Some errors found during downloading."
        else:
            out.status = "success"
            out.message = "Already downloaded."
    return out
