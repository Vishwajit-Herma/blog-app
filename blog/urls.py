from django.urls import path
from . import views
from .views import (
    BlogListGenericView,
    BlogListView,
    BlogCreateView,
    BlogDetailView,
    BlogUpdateView,
    BlogDeleteView,
    BlogDetailGenericView,
    PopularBlogListView,
    notifications_view,
)


app_name = "blog"

# urlpatterns = [
#      path("", views.blog_list, name="blog-list"),
#      path("blog-add/", views.blog_create, name="blog-add"),
#      path("blog-detail/<int:pk>", views.blog_detail, name="blog-detail"),
#      path("blog-update/<int:pk>", views.blog_update, name="blog-update"),
#      path("blog-delete/<int:pk>", views.blog_delete, name="blog-delete"),

# ]

urlpatterns = [
    path("", BlogListGenericView.as_view(), name="blog-list"),
    path("add/", BlogCreateView.as_view(), name="blog-add"),
    path("notifications/", notifications_view, name="notifications"),
    path("popular/", PopularBlogListView.as_view(), name="popular-blogs"),
    path("<slug:slug>/", BlogDetailView.as_view(), name="blog-detail"),
    path("<slug:slug>/update/", BlogUpdateView.as_view(), name="blog-update"),
    path("<slug:slug>/delete/", BlogDeleteView.as_view(), name="blog-delete"),
    path("comment/<int:pk>/delete/", views.comment_delete, name="comment-delete"),
    path("<slug:slug>/like/", views.toggle_blog_like, name="blog-like"),
    path("comment/<int:pk>/like/", views.toggle_comment_like, name="comment-like"),
]
