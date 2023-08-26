from core.shared import CommonResponse
from youtube.tasks import download_episode_yt


def download_episode(provider_shortname, episode_id) -> CommonResponse:
    out = CommonResponse()
    if provider_shortname == "yt":
        download_episode_yt.delay(episode_id=episode_id)
    out.message = "Added in queue."
    out.status = "wip"
    return out
