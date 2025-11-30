import time
from datetime import datetime

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse, HttpResponseNotModified
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.views.generic import TemplateView
from django.utils.http import http_date, parse_http_date_safe
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.core.cache import caches
from django.utils.http import quote_etag
from django.utils.http import parse_etags
from django.utils.http import http_date
from django.utils import timezone
from hashlib import sha1

from .models import Article
from .cache_utils import cache_get, cache_set

# ---------- Index (shows multiple cache headers) ----------
def index_view(request):
    """
    Demonstrates low-level cache usage with default cache
    and shows caching headers.
    """
    # Low-level: default cache
    key = "index_count"
    count = cache.get(key)
    if count is None:
        count = 1
    else:
        count += 1
    cache.set(key, count, timeout=60)
    return render(request, "index.html", {"count": count})

# ---------- Template fragment caching ----------
def fragment_view(request):
    # Generate dynamic data
    now = datetime.now()
    return render(request, "fragments.html", {"now": now})

# ---------- Low-level cache API example ----------
def low_level_cache_example(request):
    # Demonstrate multiple caches
    caches_demo = {}
    for alias in ("default", "filebased", "db", "memcached", "redis"):
        try:
            c = caches[alias]
            c.set("demo_key", f"value_from_{alias}", timeout=30)
            caches_demo[alias] = c.get("demo_key")
        except Exception as e:
            caches_demo[alias] = f"error: {e}"
    return JsonResponse(caches_demo)

# ---------- Per-view caching decorator ----------
@cache_page(20, key_prefix="perview_example")
def per_view_example(request):
    # Heavy logic simulated
    time.sleep(0.2)
    return HttpResponse("Per-view cached response (20s)")

# ---------- Class-based view caching ----------
@method_decorator(cache_page(15), name="dispatch")
class ClassBasedCacheView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["count"] = cache.get("index_count", 0)
        return ctx

# ---------- Manual invalidation ----------
def invalidate_article_cache(request, pk):
    article = get_object_or_404(Article, pk=pk)
    # Key used for per-article cache:
    key = f"article:{pk}"
    cache.delete(key)
    return JsonResponse({"deleted": key})

# ---------- ETag and Last-Modified examples ----------
def _article_etag(article):
    return quote_etag(sha1(f"{article.pk}-{article.updated_at}".encode()).hexdigest())

def etag_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    etag = _article_etag(article)
    # Check If-None-Match
    inm = request.META.get("HTTP_IF_NONE_MATCH")
    if inm:
        client_etags = parse_etags(inm)
        if etag in client_etags:
            return HttpResponseNotModified()
    # Not modified → send body with ETag header
    response = JsonResponse({"title": article.title, "updated": article.updated_at.isoformat()})
    response["ETag"] = etag
    return response

def last_modified_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    last_mod = article.updated_at
    # If-Modified-Since
    ims = request.META.get("HTTP_IF_MODIFIED_SINCE")
    if ims:
        ims_dt = parse_http_date_safe(ims)
        if ims_dt is not None and int(last_mod.timestamp()) <= ims_dt:
            return HttpResponseNotModified()
    response = JsonResponse({"title": article.title, "updated": article.updated_at.isoformat()})
    response["Last-Modified"] = http_date(last_mod.timestamp())
    return response
