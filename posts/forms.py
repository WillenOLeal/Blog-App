from django import forms
from .models import Post, Comment
from django.utils.text import slugify
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
