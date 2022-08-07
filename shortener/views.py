from django.shortcuts import redirect
from django.utils.decorators import decorator_from_middleware, method_decorator
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny

from shortener.models import UrlShortener
from shortener.serializers import UrlShortenerSerializer
from shortener.service import UrlShortenerService
from shortener.middleware import VisitorCountMiddleware


@method_decorator(decorator_from_middleware(VisitorCountMiddleware), name='retrieve')
class SharedUrlViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    ViewSet for retrieving shortened URLs with a slug and redirect to the original URL.

    Methods:
        retrieve: Redirect to the original URL.
    """
    queryset = UrlShortener.objects.all()
    serializer_class = UrlShortenerSerializer
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return redirect(instance.url)


class UrlShortenerViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    ViewSet for creating and listing shortened URLs.

    Methods:
        list: List all URLs.
        create: Create a new URL.
    """
    queryset = UrlShortener.objects.all()
    serializer_class = UrlShortenerSerializer
    permission_classes = (AllowAny,)
    service_class = UrlShortenerService

    def perform_create(self, serializer):
        """
        Create a new shortened url.
        :param serializer: UrlShortenerSerializer
        :return: None
        """
        obj = self.service_class.create(**serializer.validated_data)
        serializer.instance = obj
