from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    """The model describing the post published by the author."""
    text = models.TextField("Текст")
    pub_date = models.DateTimeField(
        "Дата публикации", auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Автор"
    )
    group = models.ForeignKey(
        "Group", on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name="groups",
        verbose_name="Группа"
    )

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return self.text[:100]


class Comment(models.Model):
    """Community post comment model."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор комментария"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Пост"
    )
    text = models.TextField("Комментарий")
    created = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text[:50]


class Follow(models.Model):
    """Subscription model for community author publications."""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Подписчик"
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="following",
        verbose_name="Блогер"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "following"],
                name="unique_pair"
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F("following")),
                name="impossible_subscribe_yourself"
            )
        ]
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"


class Group(models.Model):
    """A model describing a group for community posts."""
    title = models.CharField("Имя", max_length=200)

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return self.title[:25]
