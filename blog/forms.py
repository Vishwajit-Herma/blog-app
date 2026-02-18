from tokenize import Comment
from django import forms

from .models import Comment
from .models import Blog


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["title", "content", "image"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
