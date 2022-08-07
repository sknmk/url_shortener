from rest_framework import routers

from shortener.views import UrlShortenerViewSet, SharedUrlViewSet

router = routers.SimpleRouter()
router.register(r'r', SharedUrlViewSet)
router.register(r'shortener', UrlShortenerViewSet)

urlpatterns = router.urls
