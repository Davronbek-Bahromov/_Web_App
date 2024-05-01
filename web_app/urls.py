from django.urls import path
from .views import PostListApiView, create_post_api_view, get_post, update_post, delete_post, CreateCommentApiView, CommentListApiView, update_comment, delete_comment, LikeApiView, ListAPIView, DislikeApiView, CommentLikeApiView, CommentDislikeApiView, create_channel, get_channel,delete_channel
    
urlpatterns = [
    # url for posts
    path('create_post/', create_post_api_view,),
    path('post/', PostListApiView.as_view(), ),
    path('get_my_posts/', get_post, ),
    path('update_post/<int:pk>/', update_post, ),
    path('delete/<int:pk>/', delete_post, ),
    # url for Like and Dislike
    path('post/<int:pk>/like/', LikeApiView.as_view(), name='like'),
    path('post/<int:pk>/dislike/', DislikeApiView.as_view(), ),
    # url for comment
    path('create_comment/<int:pk>/', CreateCommentApiView.as_view(), name='create_comment'),
    path('post/<int:pk>/comment_list/', CommentListApiView.as_view(), ),
    path('update_comment/<int:pk>/', update_comment, ),
    path('delete_comment/<int:pk>/', delete_comment, name='delete_comment'),
    # url for channel
    path('create_channel/', create_channel, name='create_channel'),
    path('detail_channel/<int:pk>/', get_channel, name='detail_channel'),
    path('delete_channel/', delete_channel, name='delete_channel'),
    
]