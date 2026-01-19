import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import login_required

User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email", "posts")

class UserQuery(graphene.ObjectType):
    users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.ID(required=True))

    @login_required
    def resolve_users(root, info):
        return User.objects.all()

    @login_required
    def resolve_user(root, info, id):
        return User.objects.get(pk=id)
