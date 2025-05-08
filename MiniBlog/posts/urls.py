from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, post_list, post_create, post_edit, post_delete, post_detail, comment_delete, search

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
    # API routes
    path('api/', include(router.urls)),
    path('api/posts/<int:post_id>/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='comment-list'),
    # Template routes
    path('', post_list, name='post_list'),
    path('search/', search, name='search'),
    path('posts/new/', post_create, name='post_create'),
    path('posts/<int:pk>/', post_detail, name='post_detail'),
    path('posts/<int:pk>/edit/', post_edit, name='post_edit'),
    path('posts/<int:pk>/delete/', post_delete, name='post_delete'),
    path('comments/<int:pk>/delete/', comment_delete, name='comment_delete'),
]