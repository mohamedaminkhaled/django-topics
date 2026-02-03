# posts/schema.py
import graphene
from graphene_django import DjangoObjectType
from .models import Post
from graphene_django.filter import DjangoFilterConnectionField
from .filters import PostFilter


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        interfaces = (graphene.relay.Node,)
        fields = (
            "id",
            "title",
            "content",
            "created_at",
            "author",
        )

class PostQuery(graphene.ObjectType):
    post = graphene.relay.Node.Field(PostType)
    posts = DjangoFilterConnectionField(
        PostType,
        filterset_class=PostFilter
    )

    # def resolve_posts(root, info):
    #     return Post.objects.all()
    #
    # def resolve_post(root, info, id):
    #     return Post.objects.get(pk=id)

