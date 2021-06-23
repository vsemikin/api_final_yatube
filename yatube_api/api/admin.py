from django.contrib import admin

from .models import Comment, Group, Post


class PostAdmin(admin.ModelAdmin):
    """The model describes the fields, search and
    filters of the publication object in the admin panel."""
    list_display = ("pk", "author", "group", "text", "pub_date")
    search_fields = ("text",)
    list_filter = ("pub_date",)
    empty_value_display = "-пусто-"


class GroupAdmin(admin.ModelAdmin):
    """The model describes the fields and
    community searches in the admin panel."""
    list_display = ("pk", "title")
    search_fields = ("title",)


class CommentAdmin(admin.ModelAdmin):
    """The model allows you to moderate comments in the admin panel."""
    list_display = ("pk", "post", "author", "text", "created")
    search_fields = ("text",)
    list_filter = ("created",)


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment, CommentAdmin)
