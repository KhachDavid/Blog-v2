from django.urls import path
from django.conf.urls import url

from .views import PostListView, PostDetailView, PostCreateView, \
                    PostUpdateView, PostDeleteView, UserPostListView, \
                    CommentCreateView, CommentUpdateView, CommentDeleteView, \
                    like_post, like_comment, leaderboard, DeleteNotification, \
                    dislike_post, BestPosts 
from . import views

__author__ = "David Khachatryan"
__copyright__ = "Copyright 2021, Mat Ognutyun"
__credits__ = None
__license__ = "GPL"
__version__ = "2.0.0"
__maintainer__ = "David Khachatryan"
__email__ = "dkhachatryan@wisc.edu"
__status__ = "Production"

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comment/', CommentCreateView.as_view(), name='post-comment'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('about/', views.about, name='blog-about'),
    path('leaderboard', leaderboard, name='leaderboard'),
    path('dnotification/<int:pk>/', DeleteNotification, name='d-notification'),
    path('best-posts', BestPosts, name='best-posts'),
    path('post/<int:pk>/like', like_post, name="like_post"),
    path('post/<int:pk>/dislike', dislike_post, name="dislike_post"),
    path('post/<int:pk>/like-comment/<int:pk1>', like_comment, name="like_comment")
]