from django.core.cache import caches
from django.core.cache import cache as default_cache

def get_cache(alias="default"):
    return caches[alias]

def cache_set(alias, key, value, timeout=None, version=None):
    c = get_cache(alias)
    return c.set(key, value, timeout=timeout, version=version)

def cache_get(alias, key, version=None):
    c = get_cache(alias)
    return c.get(key, version=version)
