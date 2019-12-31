from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .models import Post, Comment, Like, Visualization
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.views.generic.list import MultipleObjectMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import PostForm, CommentForm
from django.http import JsonResponse, Http404
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
    paginate_by = 5
    context_object_name = 'posts'
    ordering = ['-published_at']


class PostDetailView(DetailView,  MultipleObjectMixin):
    model = Post
    paginate_by = 3

    def get_object(self, **kwargs):
        object = super().get_object(**kwargs)
        if self.request.user.is_authenticated:
            Visualization.objects.get_or_create(
                author=self.request.user, post=object)
        return object

    # def post(self, *args, **kwargs):
    #     form = CommentForm(self.request.POST)
    #     if form.is_valid() and form.has_changed():
    #         comment = form.instance
    #         comment.post = self.get_object()
    #         comment.author = self.request.user
    #         comment.save()
    #         return redirect('post_detail', slug=self.get_object().slug)
    #     return redirect('post_detail', slug=self.get_object().slug)

    def post(self, *args, **kwargs):
        if self.request.is_ajax():
            data = {}

            form = CommentForm(self.request.POST)
            if form.is_valid() and form.has_changed():
                comment = form.instance
                comment.post = self.get_object()
                comment.author = self.request.user
                comment.save()
                data['body'] = comment.body
                data['id'] = comment.pk

            data['success'] = True
            return JsonResponse(data)
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        object_list = Comment.objects.filter(
            post=self.get_object()).order_by('-published_at')
        context = super().get_context_data(object_list=object_list, **kwargs)
        context.update({
            'form': CommentForm()
        })
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
   # success_url = reverse_lazy('post_detail')

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

    def get_success_url(self):
        post_slug = self.kwargs['slug']
        return reverse_lazy('post_detail', kwargs={'slug': post_slug})


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
        ).order_by("-published_at")


@login_required
def like_it(request, slug):
    if request.is_ajax():
        post = get_object_or_404(Post, slug=slug)

        try:
            newCount = post.likes_count - 1
            like = Like.objects.get(author=request.user, post=post)
            like.delete()
            return JsonResponse({'newCount': newCount})

        except Like.DoesNotExist:
            Like.objects.create(author=request.user, post=post)
            return JsonResponse({'newCount': post.likes_count})
    else:
        raise Http404


@login_required
def comment_delete(request, id):
    if request.is_ajax():
        try:
            comment = Comment.objects.get(id=id)
            post = Post.objects.get(pk=comment.post.pk)
            if request.user == comment.author:
                comment.delete()
                return JsonResponse({'isDeleted': True, 'commCount': post.comments_count})
            else:
                return JsonResponse({'isDeleted': False, })
        except Comment.DoesNotExist:
            return JsonResponse({'isDeleted': False})
    else:
        raise Http404
