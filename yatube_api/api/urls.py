from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

router = DefaultRouter()
router.register(r"posts", PostViewSet)
router.register(
    r"posts/(?P<post_id>\d+)/comments", CommentViewSet, basename="Comment"
)
router.register(r"follow", FollowViewSet, basename="Follow")
router.register(r"group", GroupViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
