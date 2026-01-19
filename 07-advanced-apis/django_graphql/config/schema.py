import graphene
from posts.schema import PostQuery
from posts.mutations import CreatePost, UpdatePost, DeletePost
from users.schema import UserQuery
import graphql_jwt


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()

class Query(PostQuery, UserQuery, graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(root, info):
        return "Hello GraphQL 🚀"


schema = graphene.Schema(query=Query, mutation=Mutation)

