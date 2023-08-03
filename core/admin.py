from django.contrib import admin
from core.models import Provider, DataSource, Episode

# Register your models here.
class ProviderAdmin(admin.ModelAdmin):
    ordering = ["name"]
    list_display = ["name"]

class DataSourceAdmin(admin.ModelAdmin):
    ordering = ["name"]
    list_display = ["name", "provider"]

class EpisodeAdmin(admin.ModelAdmin):
    ordering = ["name"]
    list_display = ["name", "datasource", "is_viewed", "is_downloaded"]

admin.site.register(Provider, ProviderAdmin)
admin.site.register(DataSource, DataSourceAdmin)
admin.site.register(Episode, EpisodeAdmin)