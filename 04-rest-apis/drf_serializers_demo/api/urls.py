from django.urls import include, path
from rest_framework import routers
from .views import UserViewSet, AccountViewSet, EventViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'accounts', AccountViewSet, basename='account')
router.register(r'events', EventViewSet, basename='event')

urlpatterns = [
    path('', include(router.urls))
]
