from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token

from core.views import AddDataSourceView, DeleteDataSourceView, EpisodeView, HomepageView, PlayerView
from youtube.views import AddChannelView, DeleteChannelView

urlpatterns = [
    # Podcast
    path("", cache_page(settings.CACHE_DEFAULT_TTL)(HomepageView.as_view()), name="homepage"),
    path("player/", cache_page(settings.CACHE_DEFAULT_TTL)(PlayerView.as_view()), name="player"),
    path("episode/", cache_page(settings.CACHE_SMART_TTL)(EpisodeView.as_view()), name="episode"),
    path(
        "add-datasource/", cache_page(settings.CACHE_DEFAULT_TTL)(AddDataSourceView.as_view()), name="add-datasource"
    ),
    path(
        "delete-datasource/",
        cache_page(settings.CACHE_DEFAULT_TTL)(DeleteDataSourceView.as_view()),
        name="delete-datasource",
    ),
    *static("persist/", document_root=settings.PERSIST_AUDIO_ROOTDIR),
    # Youtube Urls
    path("yt/add-channel/", cache_page(settings.CACHE_DEFAULT_TTL)(AddChannelView.as_view()), name="yt-add-channel"),
    path(
        "yt/delete-channel/",
        cache_page(settings.CACHE_DEFAULT_TTL)(DeleteChannelView.as_view()),
        name="yt-delete-channel",
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("user-about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
    path("users/", include("verbacap.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
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
