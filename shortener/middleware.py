from shortener.service import UrlShortenerService


class VisitorCountMiddleware:
    """
    Middleware for updating the visitor count of a shortened URL.

    Methods:
        process_view: Increment the visitor count of a shortened URL.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            short_url = view_kwargs['slug']
            UrlShortenerService.increase_counter(short_url)
        except KeyError:
            pass
        return
