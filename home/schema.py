import graphene
from graphene import InputObjectType
from graphene_django import DjangoObjectType

from home.models import Post


class PostType(DjangoObjectType):
    class Meta:
        model = Post


class Query(graphene.ObjectType):
    posts = graphene.List(PostType)
    post = graphene.Field(PostType, id=graphene.Int())

    @graphene.resolve_only_args
    def resolve_posts(self):
        return Post.objects.all()

    @graphene.resolve_only_args
    def resolve_post(self, id):
        return Post.objects.get(pk=id)


class PostInput(InputObjectType):
    id = graphene.Int()
    title = graphene.String()
    description = graphene.String()


class CreatePost(graphene.Mutation):
    class Arguments:
        post_data = PostInput(required=True)

    post = graphene.Field(PostType)

    @staticmethod
    def mutate(root, info, post_data=None):
        post_instance = Post(**post_data)
        post_instance.save()
        return CreatePost(post=post_instance)  # noqa


class UpdatePost(graphene.Mutation):
    class Arguments:
        post_data = PostInput(required=True)

    post = graphene.Field(PostType)

    @staticmethod
    def mutate(root, info, post_data=None):
        post_instance = Post.objects.get(pk=post_data.id)
        if post_instance:

            post_instance.title = post_data.title
            post_instance.description = post_data.description
            post_instance.save()

            return UpdatePost(post=post_instance)  # noqa
        return UpdatePost(post=None)  # noqa


class DeletePost(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    post = graphene.Field(PostType)

    @staticmethod
    def mutate(root, info, id):
        Post.objects.get(pk=id).delete()


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
