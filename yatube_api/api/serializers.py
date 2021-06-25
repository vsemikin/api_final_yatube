from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Comment, Follow, Group, Post, User


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
        fields = ("id", "author", "post", "text", "created")
        model = Comment
        read_only_fields = ('post',)


class FollowSerializer(serializers.ModelSerializer):
    """Serializer for the Follow model."""
    # user = serializers.ReadOnlyField(source="user.username")
    user = serializers.CharField(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all()
    )

    class Meta:
        fields = ("user", "following")
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=("user", "following")
            )
        ]

    def validate(self, data):
        """The function prohibits subscribing to yourself."""
        if data["following"] == self.context["request"].user:
            raise serializers.ValidationError(
                "It is impossible to subscribe to yourself"
            )
        return data


class GroupSerializer(serializers.ModelSerializer):
    """Serializer for the Group model."""

    class Meta:
        fields = ("title",)
        model = Group
