from django.shortcuts import render, redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordResetConfirmView, PasswordResetCompleteView,
                                       PasswordResetView, PasswordResetDoneView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, UpdateCustomUser, UpdateProfile


class CustomSignUp(SuccessMessageMixin, CreateView):
    template_name = 'accounts/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    success_message = "Thank you for joining %(username)s!"


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'accounts/logout.html'


class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    success_url = reverse_lazy('password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'


@login_required
def user_profile(request):
    """ Profile page for the user, Renders 2 forms, one for username and password,
    and the other for the image upload """
    form = UpdateCustomUser(request.POST or None, instance=request.user)
    profile_form = UpdateProfile(request.POST or None, request.FILES or None, instance=request.user.profile)

    if form.is_valid() and profile_form.is_valid():
        form.clean_username()
        form.clean_email()
        form.save()
        profile_form.save()
        messages.success(request, 'Your profile was updated successfully!')
        return redirect('profile')

    context = {
        'form': form,
        'profile_form': profile_form
    }

    return render(request, 'accounts/profile.html', context)


@login_required
def user_delete(request):
    try:
        user = get_user_model().objects.get(id=request.user.id)
        user.delete()
        messages.success(request, 'Your account was deleted successfully')
        return redirect('login')
    except get_user_model().DoesNotExist:
        messages.error(request, 'Profile deletion failed')
        return redirect('profile')


@login_required
def reset_profile_picture(request):
    try:
        user = get_user_model().objects.get(id=request.user.id)
        if user.profile.picture:
            pic_url = user.profile.picture.url
            if pic_url != '/media/default.jpg':
                user.profile.picture.delete()
            return redirect('profile')
        return redirect('profile')
    except:
        messages.error(request, 'Failed')
        return redirect('profile')
