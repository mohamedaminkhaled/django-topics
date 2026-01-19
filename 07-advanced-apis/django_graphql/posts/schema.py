# posts/schema.py
import graphene
from graphene_django import DjangoObjectType
from .models import Post


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ("id", "title", "content", "created_at", "author")

class PostQuery(graphene.ObjectType):
    posts = graphene.List(PostType)
    post = graphene.Field(PostType, id=graphene.ID(required=True))

    def resolve_posts(root, info):
        return Post.objects.all()

    def resolve_post(root, info, id):
        return Post.objects.get(pk=id)

