from django.contrib import admin
from .models import Blog, PopularBlog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):

    list_display = ("title", "author", "created_at", "updated_at")

    readonly_fields = ("created_at", "updated_at")

    ordering = ("-created_at",)


@admin.register(PopularBlog)
class PopularBlogAdmin(admin.ModelAdmin):
    list_display = ("title", "views", "created_at")