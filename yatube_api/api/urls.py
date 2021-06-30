from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

router = DefaultRouter()
router.register("posts", PostViewSet, basename="Post")
router.register(
    r"posts/(?P<post_id>\d+)/comments", CommentViewSet, basename="Comment"
)
router.register("follow", FollowViewSet, basename="Follow")
router.register("group", GroupViewSet, basename="Group")

urlpatterns = [
    path("v1/", include([
        path("", include(router.urls)),
        path("token/", include([
            path("", TokenObtainPairView.as_view(), name="token_obtain_pair"),
            path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
        ])),
    ])),
]
