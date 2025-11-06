from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Account, Event, GameRecord
from django.contrib.auth import get_user_model
User = get_user_model()


# Basic Serializer
class BasicUserSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']
        extra_kwargs = {
            'url': {'view_name': 'user-detail', 'lookup_field': 'username'}
        }

# --- Custom Field Example -------------------------------------------------
class UppercaseCharField(serializers.CharField):
    """Simple custom field that stores uppercase strings."""
    def to_internal_value(self, data):
        value = super().to_internal_value(data)
        return value.upper()

# --- Simple Serializer (non-model) ---------------------------------------
class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()

    def create(self, validated_data):
        # return a plain object or hook to model creation
        return validated_data


# --- Field-level validator (function) ------------------------------------
def multiple_of_ten(value):
    if value % 10 != 0:
        raise serializers.ValidationError('Not a multiple of ten')


# --- Class-based validator example --------------------------------------
class EvenNumberValidator:
    def __init__(self, message=None):
        self.message = message or 'Number must be even.'

    def __call__(self, value):
        if value % 2 != 0:
            raise serializers.ValidationError(self.message)


# --- GameRecord serializer with validators --------------------------------
class GameRecordSerializer(serializers.ModelSerializer):
    score = serializers.IntegerField(validators=[multiple_of_ten, EvenNumberValidator()])

    class Meta:
        model = GameRecord
        fields = ['id', 'player', 'score', 'played_at']
        read_only_fields = ['played_at']


# --- Writable nested serializer example ----------------------------------
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'room_number', 'date']
        validators = [
            UniqueTogetherValidator(
                queryset=Event.objects.all(),
                fields=['room_number', 'date']
            )
        ]

# --- Nested vs depth example ---------------------------------------------
class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class AccountSerializerDepth(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_name', 'users', 'created']
        depth = 1

# --- Explicit nested serializer (preferred for control) ------------------
class AccountUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class AccountSerializer(serializers.HyperlinkedModelSerializer):
    # demonstrate custom URL field + context usage
    url = serializers.HyperlinkedIdentityField(view_name='account-detail', lookup_field='slug')
    users = serializers.HyperlinkedRelatedField(
        view_name='user-detail', lookup_field='username', many=True, read_only=True
    )

    # show SerializerMethodField and custom field
    # DRF automatically looks for a method named get_<fieldname>()
    primary_user = serializers.SerializerMethodField(read_only=True)
    name_upper = UppercaseCharField(source='account_name', required=False)

    class Meta:
        model = Account
        fields = ['url', 'account_name', 'slug', 'name_upper', 'primary_user', 'users', 'created']
        extra_kwargs = {
            'users': {'lookup_field': 'username'}
        }

    def get_primary_user(self, obj):
        # example of using context
        request = self.context.get('request')
        # pick first user as primary for demo
        first = obj.users.first()
        return first.username if first else None

# --- ListSerializer / bulk create example -------------------------------
class BulkAccountListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        # bulk create accounts (uses model .objects.bulk_create)
        accounts = [Account(**item) for item in validated_data]
        Account.objects.bulk_create(accounts)
        return accounts


class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['account_name', 'slug']
        list_serializer_class = BulkAccountListSerializer

# --- BaseSerializer minimal example -------------------------------------
class ReadOnlyNameSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {'name': instance.account_name}

# --- Overriding save directly -------------------------------------------
class ContactSerializer(serializers.Serializer):
    email = serializers.EmailField()
    message = serializers.CharField()

    def save(self, **kwargs):
        # custom behavior instead of creating model
        email = self.validated_data['email']
        message = self.validated_data['message']
        # pretend to send email here
        return {'sent_to': email, 'message': message}

