from django.db import models
from django.contrib.auth import get_user_model


class Post(models.Model):
    """ Post has a many-to-one relationship with its respective User"""
    thumbnail = models.ImageField()
    title = models.CharField(max_length=100)
    body = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} by {self.author.username}'


class Comment(models.Model):
    """ Comment has a many-to-one relationship with both User and Post """
    authror = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}'s comment"


class Like(models.Model):
    """ Like has a many-to-one relationship with both User and Post """
    authror = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author.username} liked it'


class Visualization(models.Model):
    """ Visualization has a many-to-one relationship with both User and Post """
    authror = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author.username} viewed it'
