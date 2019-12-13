from django.urls import path
from . import views
from .views import (PostCreateView, PostListView,
                    PostDetailView, PostUpdateView,
                    PostDeleteView)

urlpatterns = [
    path('', views.PostListView.as_view(), name="post_list"),
    path('search/', views.SearchResultView.as_view(), name="post_search"),
    path('posts/<slug>/', views.PostDetailView.as_view(), name="post_detail"),
    path('create-post/', views.PostCreateView.as_view(), name="post_create"),
    path('<slug>/update-post/', views.PostUpdateView.as_view(), name="post_update"),
    path('<slug>/delete-post/', views.PostDeleteView.as_view(), name="post_delete"),
    path('like/<slug>', views.like_it, name="post_like"),
]
