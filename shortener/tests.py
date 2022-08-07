from django.test import TestCase
from django.urls import reverse

from shortener.models import UrlShortener
from shortener.service import UrlShortenerService


class UrlShortenerViewTestCase(TestCase):
    def setUp(self):
        self.test_long_url_1 = 'https://www.example2.com'
        self.test_long_url_2 = 'https://www.example.com'
        self.test_object = UrlShortener.objects.create(
            url=self.test_long_url_1,
            slug='12345',
            visitor_count=0
        )

    def test_create_shortened_url(self):
        url = reverse('urlshortener-list')
        payload = {'url': self.test_long_url_2}
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['url'], self.test_long_url_2)
        self.assertIsNotNone(response.data['slug'])
        self.assertEqual(response.data['visitor_count'], 0)

    def test_get_shortened_url(self):
        short_url = self.test_object.slug
        response = self.client.get('/r/{}/'.format(short_url))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.test_object.url)

        # try for a non-existent slug
        response = self.client.get('/r/{}/'.format('non-exist'))
        self.assertEqual(response.status_code, 404)

    def test_list_shortened_urls(self):
        url = reverse('urlshortener-list')
        payload = {'url': self.test_long_url_2}
        response = self.client.post(url, payload)
        get_w_slug_url = reverse(
            'urlshortener-detail',
            kwargs=dict(slug=response.data['slug'])
        )
        # increase visitor count of the shortened URL twice.
        self.client.get(get_w_slug_url)
        self.client.get(get_w_slug_url)

        short_url = response.data['slug']
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['url'], self.test_long_url_2)
        self.assertEqual(response.data[0]['slug'], short_url)
        self.assertEqual(response.data[0]['visitor_count'], 2)


class UrlShortenerServiceTestCase(TestCase):
    def setUp(self):
        self.service_class = UrlShortenerService
        self.test_long_url_1 = 'https://example.com'
        self.test_long_url_2 = 'https://example2.com'
        self.test_object = UrlShortener.objects.create(
            url=self.test_long_url_1,
            slug='abcABC',
            visitor_count=1
        )

    def test_increase_counter(self):
        self.service_class.increase_counter(self.test_object.slug)
        self.test_object.refresh_from_db()
        self.assertEqual(self.test_object.visitor_count, 2)

    def test_create(self):
        self.service_class.create(url=self.test_long_url_1)
        self.service_class.create(url=self.test_long_url_2)
        self.assertEqual(UrlShortener.objects.count(), 3)
