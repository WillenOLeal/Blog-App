from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .models import Post, Comment, Like, Visualization
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import PostForm
from django.http import HttpResponseRedirect
from django.db.models import Q


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'post_action': 'create'
        })
        return context


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    ordering = ['-published_at']


class PostDetailView(DetailView):
    model = Post

    def get_object(self, **kwargs):
        object = super().get_object(**kwargs)
        if self.request.user.is_authenticated:
            Visualization.objects.get_or_create(
                author=self.request.user, post=object)
        return object


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('post_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'post_action': 'update'
        })
        return context

    def test_func(self):
        post = self.get_object()
        if post.author == self.request.user:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')
    success_message = "Post deleted successfully."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def test_func(self):
        post = self.get_object()
        if post.author == self.request.user:
            return True
        return False


class SearchResultView(ListView):
    model = Post
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('search_string')
        return Post.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )


@login_required
def like_it(request, slug):
    post = get_object_or_404(Post, slug=slug)
    try:
        like = Like.objects.get(author=request.user, post=post)
        like.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Like.DoesNotExist:
        Like.objects.create(author=request.user, post=post)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
