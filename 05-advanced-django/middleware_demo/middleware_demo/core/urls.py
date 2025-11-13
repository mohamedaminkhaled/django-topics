from django.urls import path, re_path
from . import views

urlpatterns = [
    path("hello/", views.hello_view, name="hello"),
    path("error/", views.error_view, name="error"),
    path("template/", views.template_view, name="template"),
    re_path(r"^\.well-known/(?P<path>.*)$", views.well_known_file),
]
