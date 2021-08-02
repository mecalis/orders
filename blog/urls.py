from django.urls import path
from .views import (
    blog_post_detail_view,
    blog_post_list_view,
    blog_post_update_view,
    blog_post_delete_view,
    blog_post_create_view,
    blog_post_count_view,
)

app_name = 'blog'

urlpatterns = [
    path('', blog_post_list_view, name = 'blog-home'),
    path('blog-new/', blog_post_create_view, name = 'blog-new'),
    path('blog-count/', blog_post_count_view, name = 'blog-count'),
    path('<str:slug>/', blog_post_detail_view, name = 'blog-detail'),
    path('<str:slug>/edit/', blog_post_update_view, name = 'blog-edit'),
    path('<str:slug>/delete/', blog_post_delete_view, name = 'blog-delete'),
]
