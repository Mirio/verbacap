from django.contrib import admin

from core.models import DataSource, Episode, Playlist, Provider


# Register your models here.
@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    ordering = ["name"]
    list_display = ["name"]


@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    ordering = ["name"]
    list_display = ["name", "provider"]


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    ordering = ["name"]
    list_display = ["name", "datasource", "is_viewed", "is_downloaded"]


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    ordering = ["order_num"]
    list_display = ["order_num", "episode"]
