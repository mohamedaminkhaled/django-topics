import graphene
from .models import Post
from .schema import PostType
from graphql_jwt.decorators import login_required


class CreatePost(graphene.Mutation):
    post = graphene.Field(PostType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)

    @login_required
    def mutate(self, info, title, content):
        user = info.context.user
        if user.is_anonymous:
            return CreatePost(
                success=False,
                errors=["Authentication required"],
                post=None
            )

        post = Post.objects.create(
            title=title,
            content=content,
            author=user
        )

        return CreatePost(
            post=post,
            success=True,
            errors=None
        )

class UpdatePost(graphene.Mutation):
    post = graphene.Field(PostType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        content = graphene.String()

    def mutate(self, info, id, title=None, content=None):
        user = info.context.user
        try:
            post = Post.objects.get(pk=id)
        except Post.DoesNotExist:
            return UpdatePost(success=False, errors=["Post not found"])

        if post.author != user:
            return UpdatePost(
                success=False,
                errors=["Not allowed"]
            )

        post.save()

        return UpdatePost(success=True, errors=None, post=post)

class DeletePost(graphene.Mutation):
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, id):
        user = info.context.user
        try:
            post = Post.objects.get(pk=id)
        except Post.DoesNotExist:
            return DeletePost(
                success=False,
                errors=["Post not found"]
            )

        if post.author != user:
            return DeletePost(
                success=False,
                errors=["Not allowed"]
            )

        post.delete()
        return DeletePost(success=True, errors=None)
