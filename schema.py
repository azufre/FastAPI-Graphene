import graphene

from models.comment import Comments
from models.post import Post
from models.user import User
from serializers import (CommentGrapheneInputModel, CommentGraphModel,
                         PostGrapheneInputModel, PostGraphModel,
                         UserGrapheneInputModel, UserGraphModel)


class Query(graphene.ObjectType):
    say_hello = graphene.String(
        name=graphene.String(default_value="Test driven"))

    list_users = graphene.List(UserGraphModel)

    get_single_user = graphene.Field(UserGraphModel, user_id=graphene.NonNull(graphene.Int))

    @staticmethod
    def resolve_say_hello(parent, info, name):
        return f'Hello {name}'

    @staticmethod
    def resolve_list_users(parent, info):
        return User.all()

    @staticmethod
    def resolve_get_single_user(parent, info, user_id):
        return User.find_or_fail(user_id)

class CreateUser(graphene.Mutation):
    class Arguments:
        user_details = UserGrapheneInputModel()

    Output = UserGraphModel

    @staticmethod
    def mutate(parent, info, user_details):
        user = User()
        user.name = user_details.name
        user.address = user_details.address
        user.phone_number = user_details.phone_number
        user.sex = user_details.sex

        user.save()

        return user


class CreatePost(graphene.Mutation):
    class Arguments:
        post_details = PostGrapheneInputModel()

    Output = PostGraphModel

    @staticmethod
    def mutate(parent, info, post_details):
        user = User.find_or_fail(post_details.user_id)
        post = Post()
        post.title = post_details.title
        post.body = post_details.body

        user.posts().save(post)

        return post


class CreateComment(graphene.Mutation):
    class Arguments:
        comment_details = CommentGrapheneInputModel()

    Output = CommentGraphModel

    @staticmethod
    def mutate(parent, info, comment_details):
        user = User.find_or_fail(comment_details.user_id)
        post = Post.find_or_fail(comment_details.post_id)

        comment = Comments()

        comment.body = comment_details.body

        user.comments().save(comment)
        post.comments().save(comment)

        return comment

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_post = CreatePost.Field()
    create_comment = CreateComment.Field()