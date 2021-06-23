from rest_framework import serializers

from .models import Comment, Group, Follow, Post


class PostSerializer(serializers.ModelSerializer):
    """Serializer for the Post model."""
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        fields = ("id", "text", "author", "pub_date")
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for the Comment model."""
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        fields = ("id", "author", "text", "created")
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    """Serializer for the Follow model."""
    user = serializers.ReadOnlyField(source="user.username")
    following = serializers.ReadOnlyField(source="author.username")

    class Meta:
        fields = ("user", "following")
        model = Follow


class GroupSerializer(serializers.ModelSerializer):
    """Serializer for the Group model."""

    class Meta:
        fields = ("title",)
        model = Group
