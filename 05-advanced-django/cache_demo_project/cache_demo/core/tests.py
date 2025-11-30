from django.test import TestCase, Client
from django.core.management import call_command
from django.core.cache import caches
from .models import Article

class CacheTests(TestCase):
    def setUp(self):
        # Create DB cache table if using local test DB
        try:
            call_command("createcachetable", "cache_table")
        except Exception:
            pass
        self.client = Client()

    def test_per_view_cache(self):
        r1 = self.client.get("/perview/")
        r2 = self.client.get("/perview/")
        self.assertEqual(r1.content, r2.content)

    def test_fragment_cache(self):
        r1 = self.client.get("/fragment/")
        r2 = self.client.get("/fragment/")
        self.assertIn(b"CACHED BLOCK", r2.content)

    def test_low_level_caches(self):
        # ensure each configured alias returns something (or error string)
        aliases = ["default", "filebased", "db", "memcached", "redis"]
        r = self.client.get("/lowlevel/")
        data = r.json()
        for a in aliases:
            self.assertIn(a, data)

    def test_etag_not_modified(self):
        art = Article.objects.create(title="T", content="X")
        r1 = self.client.get(f"/etag/{art.pk}/")
        etag = r1.headers.get("ETag")
        r2 = self.client.get(f"/etag/{art.pk}/", HTTP_IF_NONE_MATCH=etag)
        self.assertEqual(r2.status_code, 304)
