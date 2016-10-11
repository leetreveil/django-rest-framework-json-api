from django.conf.urls import include, url
from rest_framework import routers

from example.views import BlogViewSet, EntryViewSet, AuthorViewSet, CommentViewSet, ProfileDatumViewSet

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'blogs', BlogViewSet)
router.register(r'entries', EntryViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'datum', ProfileDatumViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
