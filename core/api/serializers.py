from rest_framework import serializers

from core.models import DataSource, Episode, Playlist, Provider


class CommonSuccessSerializer(serializers.Serializer):
    success = serializers.BooleanField()


class CommonSerializer(serializers.Serializer):
    status = serializers.StringRelatedField
    message = serializers.StringRelatedField
    value = serializers.StringRelatedField


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = "__all__"


class DataSourceSerializer(serializers.ModelSerializer):
    provider = ProviderSerializer(read_only=True)

    class Meta:
        model = DataSource
        fields = "__all__"


class EpisodeSerializer(serializers.ModelSerializer):
    datasource = DataSourceSerializer(read_only=True)

    class Meta:
        model = Episode
        fields = "__all__"


class PlaylistSerializer(serializers.ModelSerializer):
    episode = EpisodeSerializer(read_only=True)

    class Meta:
        model = Playlist
        fields = "__all__"
