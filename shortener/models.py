from django.db import models


class UrlShortener(models.Model):
    url = models.URLField()
    slug = models.SlugField(unique=True)
    visitor_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug

    class Meta:
        ordering = ('-created_at',)
