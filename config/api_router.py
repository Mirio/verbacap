from django.urls import path
from rest_framework.routers import SimpleRouter

from core.api.views import EpisodeSerializerViewSet, EpisodeViewedSerializer, PlaylistEditView, PlaylistView
from verbacap.users.api.views import UserViewSet

router = SimpleRouter()

router.register("users", UserViewSet)
router.register("episode", EpisodeSerializerViewSet, "episode")

app_name = "api"
urlpatterns = [
    path("playlist/", PlaylistView.as_view(), name="playlist"),
    path("playlist/edit/<str:provider_shortname>/<str:episode_id>/", PlaylistEditView.as_view(), name="playlist-edit"),
    path(
        "episode/viewed/<str:provider_shortname>/<str:episode_id>/",
        EpisodeViewedSerializer.as_view(),
        name="episode-viewed",
    ),
] + router.urls
