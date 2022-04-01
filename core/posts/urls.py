

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from posts.views import Posts, Votes, PostsCreate, PostUpdateDelete, \
    CommentOnImage, GetCommentImage, SearchTags

app_name = 'posts-app'

urlpatterns = [
    path("post-create/", PostsCreate.as_view(), name = "post-create-url"),
    
    path("posts/<int:id>/", PostUpdateDelete.as_view(), name = "posts-update-url"),
 
    path("posts-all/", Posts.as_view(), name = "posts-url"),

    path('vote/<int:post_id>/', Votes.as_view(), name="votes-url"),
    
    path("all-comments/", CommentOnImage.as_view(), name="all-comments-url"),
    
    path("comments/<int:post_id>/", GetCommentImage.as_view(), name="get-comment-image-url"),
    
    path("comments/<int:post_id>/<int:comment_id>/", CommentOnImage.as_view(), name="comment-image-url")
    ,
    
    path("search-tags/<str:tag>/", SearchTags.as_view(), name="search-query_url"),
    
    
    
    
]    