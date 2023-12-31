from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    enabled = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Provider(BaseModel):
    name = models.CharField(help_text="Provider name", unique=True)
    icon = models.CharField(help_text="Font Awesome icon, insert full html")
    color = models.CharField(help_text="HexColor to apply on the icon", default="#fff")
    shortname = models.CharField(help_text="Prefix for the audio files", default="000")

    def __str__(self):
        return self.name


class DataSource(BaseModel):
    name = models.CharField(help_text="Name of this datasource")
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, help_text="Provider to use")
    target = models.CharField(help_text="Target url/string based by the provider type")

    def __str__(self):
        return f"{self.provider.name}/{self.name}"


class Episode(BaseModel):
    episode_id = models.CharField(help_text="Episode ID (i.e Youtube ID)", unique=True)
    name = models.CharField(help_text="Episode Name")
    datasource = models.ForeignKey(DataSource, on_delete=models.CASCADE, help_text="Datasource to use")
    episode_date = models.DateField()
    current_time = models.IntegerField(default=0, help_text="Current time (for resume function)")
    target = models.CharField(help_text="Episode target url/string based by Provider")
    is_viewed = models.BooleanField(default=False)
    is_downloaded = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.datasource.provider.name}/{self.datasource.name}/{self.name}"


class Playlist(BaseModel):
    order_num = models.SmallIntegerField()
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.episode.name}"


class Settings(BaseModel):
    name = models.CharField(help_text="Settings Name", unique=True)
    value = models.CharField(help_text="Value of the setting")

    def __str__(self):
        return f"{self.name}"
