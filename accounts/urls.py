from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.CustomSignUp.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('password-reset', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/', views.user_profile, name='profile'),
    path('profile-delete/', views.user_delete, name='profile_delete'),
    #path('profile-picture-delete/', views.reset_profile_picture, name='profile_reset_picture'),

]
