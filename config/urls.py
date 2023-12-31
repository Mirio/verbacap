from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token

from core.views import (
    Core_AddDataSourceView,
    Core_DeleteDataSourceView,
    Core_EpisodeView,
    Core_HealthView,
    Core_HomepageView,
    Core_PlayerView,
    Core_PlaylistView,
    Core_Settings,
)
from spreaker.views import Spreaker_AddPodcastView, Spreaker_DeletePodcastView
from youtube.views import (
    Youtube_AddChannelView,
    Youtube_AddPlaylistView,
    Youtube_DeleteChannelView,
    Youtube_DeletePlaylistView,
)

urlpatterns = [
    # Podcast
    path("", Core_HomepageView.as_view(), name="homepage"),
    path("player/", Core_PlayerView.as_view(), name="player"),
    path("episode/", Core_EpisodeView.as_view(), name="episode"),
    path("settings/", Core_Settings.as_view(), name="settings"),
    path("playlist/", Core_PlaylistView.as_view(), name="playlist"),
    path(
        "add-datasource/",
        Core_AddDataSourceView.as_view(),
        name="add-datasource",
    ),
    path(
        "delete-datasource/",
        Core_DeleteDataSourceView.as_view(),
        name="delete-datasource",
    ),
    *static("persist/", document_root=settings.PERSIST_AUDIO_ROOTDIR),
    # Youtube Urls
    path(
        "yt/add-channel/",
        Youtube_AddChannelView.as_view(),
        name="yt-add-channel",
    ),
    path(
        "yt/delete-channel/",
        Youtube_DeleteChannelView.as_view(),
        name="yt-delete-channel",
    ),
    path(
        "yt/add-playlist/",
        Youtube_AddPlaylistView.as_view(),
        name="yt-add-playlist",
    ),
    path(
        "yt/delete-playlist/",
        Youtube_DeletePlaylistView.as_view(),
        name="yt-delete-playlist",
    ),
    # Spreaker Urls
    path(
        "sk/add-podcast/",
        Spreaker_AddPodcastView.as_view(),
        name="sk-add-podcast",
    ),
    path(
        "sk/delete-podcast/",
        Spreaker_DeletePodcastView.as_view(),
        name="sk-delete-podcast",
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("user-about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
    path("users/", include("verbacap.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    path("-/health/", Core_HealthView.as_view(), name="health_check"),
    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
