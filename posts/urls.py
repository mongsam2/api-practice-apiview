from django.urls import path
from .views import Posts, PostsDetail

urlpatterns = [
    path("", Posts.as_view()),
    path("<int:post_id>/", PostsDetail.as_view()),
]