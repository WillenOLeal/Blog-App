from django import forms
from .models import Post
from django.utils.text import slugify
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body')

    def clean_title(self):
        title = self.cleaned_data['title']
        slug = slugify(title)
        if Post.objects.filter(slug=slug).exists():
            raise ValidationError('A Post with this title already exists.')
        return title
