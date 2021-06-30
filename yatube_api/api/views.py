from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from .models import Group, Post
from .permissions import IsOwnerOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    """The class returns all community posts or creates a new post or
    modifies a post."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("group",)

    def perform_create(self, serializer):
        """The function passes the current user as the author of the post
        published from his profile."""
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """The class returns all the comments of the post or
    creates a comment on the post or modifies the comment."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        """The function returns a queryset filtered by the post id
        from the URL."""
        post = self.get_post()
        return post.comments.all()

    def get_post(self):
        """The function returns the post whose id is obtained from the URL."""
        post_id = self.kwargs["post_id"]
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
    filter_backends = (filters.SearchFilter,)
    search_fields = ("=user__username", "=following__username")

    def get_queryset(self):
        """The function returns a queryset containing all subscribers
        of the current user."""
        return self.request.user.following.all()

    def perform_create(self, serializer):
        """The function passes the current user as a subscriber to the
        specified blogger."""
        serializer.save(user=self.request.user)


class GroupViewSet(CreateListViewSet):
    """The class returns a list of all groups and creates a new group."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
