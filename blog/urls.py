from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, \
    CommentCreateView, CommentUpdateView, CommentDeleteView, LikeView, CommentLikeView, leaderboard, DeleteNotification, \
        BestPosts
from . import views

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
    path('like/<int:pk>', LikeView, name='like-post'),
    path('like/comment/<int:pk>', CommentLikeView, name='like-comment'),
    path('leaderboard', leaderboard, name='leaderboard'),
    path('dnotification/<int:pk>/', DeleteNotification, name='d-notification'),
    path('best-posts', BestPosts, name='best-posts')
]