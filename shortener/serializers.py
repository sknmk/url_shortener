from rest_framework import serializers

from shortener.models import UrlShortener


class UrlShortenerSerializer(serializers.ModelSerializer):
    """
    Serializer for UrlShortener model.

    Fields:
        url (str): URL to be shortened.
        slug (str): Shortened URL.
        visitor_count (int): Number of times the URL has been visited.
    """
    url = serializers.URLField()
    slug = serializers.SlugField(read_only=True)
    visitor_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = UrlShortener
        lookup_field = 'slug'
        fields = ('url', 'slug', 'visitor_count')
