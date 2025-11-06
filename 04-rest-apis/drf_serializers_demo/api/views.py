from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Account, Event, GameRecord
from .serializers import (
    AccountSerializer, AccountSerializerDepth, AccountCreateSerializer,
    EventSerializer, GameRecordSerializer, ContactSerializer, BasicUserSerializer
)
from django.contrib.auth import get_user_model
User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = BasicUserSerializer
    lookup_field = 'username'

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_field = 'slug'

    @action(detail=True, methods=['get'])
    def users_list(self, request, slug=None):
        account = self.get_object()
        users = account.users.all()
        return Response([u.username for u in users])

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class GameRecordViewSet(viewsets.ModelViewSet):
    queryset = GameRecord.objects.all()
    serializer_class = GameRecordSerializer
