from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404

from .models import Group, Post
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    """The class returns all community posts or creates a new post or
    modifies a post."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        """The function passes the current user as the author of the post
        published from his profile."""
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """The class returns all the comments of the post or
    creates a comment on the post or modifies the comment."""
    serializer_class = CommentSerializer

    def get_queryset(self):
        """The function returns a queryset filtered by the post id
        from the URL."""
        post = self.get_post()
        return post.comments.all()

    def get_post(self):
        """The function returns the post whose id is obtained from the URL."""
        post_id = self.kwargs['post_id']
        return get_object_or_404(Post, id=post_id)

    def perform_create(self, serializer):
        """The function adds the current user and the number of the commented post
        as comment fields when creating it."""
        serializer.save(author=self.request.user, post=self.get_post())


class CreateListViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """Custom view set for creating an object and getting a list of objects."""
    pass


class FollowViewSet(CreateListViewSet):
    """The class returns a list of all subscribers and
    creates a subscription."""
    serializer_class = FollowSerializer

    def get_queryset(self):
        """."""
        username_ = self.request.user.username
        user_ = get_object_or_404(User, username=username_)
        return user_.following.all()

    def perform_create(self, serializer):
        """."""
        serializer.save(user=self.request.user)


class GroupViewSet(CreateListViewSet):
    """The class returns a list of all groups and creates a new group."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
