from django.urls import path
from rest_framework.routers import SimpleRouter

from core.api.views import (
    Action_AppCacheCleanupView,
    EpisodeSerializerViewSet,
    EpisodeViewedView,
    PlaylistEditView,
    PlaylistView,
    Task_CoreCalcolatePersistInfoView,
)
from spreaker.api.views import Task_SK_ImportEpisodeSK
from verbacap.users.api.views import UserViewSet
from youtube.api.views import Task_YT_ImportEpisodesYTChannel, Task_YT_ImportEpisodesYTPlaylist

router = SimpleRouter()

router.register("users", UserViewSet)
router.register("episode", EpisodeSerializerViewSet, "episode")

app_name = "api"
urlpatterns = [
    path("action/core-deleteappcache/", Action_AppCacheCleanupView.as_view(), name="api-action-appcachecleanup"),
    path(
        "task/yt-importepisodeschannel/",
        Task_YT_ImportEpisodesYTChannel.as_view(),
        name="api-task-yt-importepisodeschannel",
    ),
    path(
        "task/yt-importepisodesplaylist/",
        Task_YT_ImportEpisodesYTPlaylist.as_view(),
        name="api-task-yt-importepisodesplaylist",
    ),
    path("task/sk-importepisodes/", Task_SK_ImportEpisodeSK.as_view(), name="api-task-sk-importepisodes"),
    path(
        "task/core-calcolatepersistinfo/",
        Task_CoreCalcolatePersistInfoView.as_view(),
        name="api-task-corecalcolatepersistinfo",
    ),
    path("playlist/", PlaylistView.as_view(), name="api-playlist"),
    path(
        "playlist/edit/<str:provider_shortname>/<str:episode_id>/",
        PlaylistEditView.as_view(),
        name="api-playlist-edit",
    ),
    path(
        "episode/viewed/<str:provider_shortname>/<str:episode_id>/",
        EpisodeViewedView.as_view(),
        name="api-episode-viewed",
    ),
] + router.urls
