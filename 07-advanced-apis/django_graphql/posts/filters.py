import django_filters
from .models import Post


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    content = django_filters.CharFilter(lookup_expr="icontains")
    author_username = django_filters.CharFilter(
        field_name="author__username",
        lookup_expr="icontains"
    )

    class Meta:
        model = Post
        fields = ["title", "author_username"]
