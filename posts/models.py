from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import uuid


class Post(models.Model):
    """ Post has a many-to-one relationship with its respective User"""
    title = models.CharField(max_length=100)
    body = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(
        editable=False, max_length=100, unique=True, null=False)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} by {self.author.username}'

    def save(self, *args, **kwargs):
        post_title = self.title
        slug = slugify(post_title, allow_unicode=True)
        self.slug = slug + '-' + str(uuid.uuid4())
        super().save(*args, **kwargs)

    @property
    def likes_count(self):
        return self.like_set.all().count()

    @property
    def comments_count(self):
        return self.comment_set.all().count()

    @property
    def views_count(self):
        return self.visualization_set.all().count()


class Comment(models.Model):
    """ Comment has a many-to-one relationship with both User and Post """
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}'s comment"


class Like(models.Model):
    """ Like has a many-to-one relationship with both User and Post """
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author.username} liked it'


class Visualization(models.Model):
    """ Visualization has a many-to-one relationship with both User and Post """
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author.username} viewed it'
