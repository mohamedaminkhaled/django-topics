from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("fragment/", views.fragment_view, name="fragment"),
    path("lowlevel/", views.low_level_cache_example, name="lowlevel"),
    path("perview/", views.per_view_example, name="perview"),
    path("classview/", views.ClassBasedCacheView.as_view(), name="classview"),
    path("invalidate/<int:pk>/", views.invalidate_article_cache, name="invalidate"),
    path("etag/<int:pk>/", views.etag_view, name="etag"),
    path("lastmod/<int:pk>/", views.last_modified_view, name="lastmod"),
]
