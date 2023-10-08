from core.shared import CommonResponse
from spreaker.tasks import download_episode_sk
from youtube.tasks import download_episode_yt


def download_episode(provider_shortname, episode_id) -> CommonResponse:
    out = CommonResponse()
    if provider_shortname in ["yt", "yt-playlist"]:
        download_episode_yt.delay(episode_id=episode_id)
    if provider_shortname == "sk":
        download_episode_sk.delay(episode_id=episode_id)
    out.message = "Added in queue."
    out.status = "wip"
    return out
