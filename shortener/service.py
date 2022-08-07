from django.db.models import F
from django.utils.crypto import get_random_string

from shortener.models import UrlShortener


class UrlShortenerService:
    """
    Service for creating and updating shortened URLs.

    Methods:
        create: Create a new URL.
        increase_counter: Increment the visitor count of a shortened URL.

    """

    @staticmethod
    def increase_counter(slug):
        """
        Increment the visitor count of a shortened URL.
        :param slug: string
        :return: None
        """

        UrlShortener.objects.filter(slug=slug).update(visitor_count=F('visitor_count') + 1)
        return

    @staticmethod
    def create(**kwargs):
        """
        Create a new shortened url with a unique slug. Works with the UrlShortenerViewSet view and the
        UrlShortenerSerializer serializer's validated data. slug is generated randomly and the shortened URLs are
        stored in the database. Default visitor_count 0.
        :param kwargs: **kwargs
        :return: UrlShortener
        """
        length = 3
        while True:
            slug = get_random_string(length=length+1)
            if not UrlShortener.objects.filter(slug=slug).exists():
                break
        return UrlShortener.objects.create(slug=slug, **kwargs)
