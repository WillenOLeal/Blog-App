from django import forms
from .models import CustomUser, Profile
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

    def clean_username(self):
        """ Check if username already exists (is case sensitive"""
        username = self.cleaned_data['username']
        try:
            result = get_user_model().objects.get(username__iexact=username)
        except get_user_model().DoesNotExist:
            return username
        raise forms.ValidationError(f'Username "{username}" is already in use.')

    def clean_email(self):
        """ Convert all emails to lowercase befor saving """
        email = self.cleaned_data['email']
        return email.lower()


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class UpdateCustomUser(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']

    def clean_username(self):
        """ Check if username already exists (is case sensitive"""
        username = self.cleaned_data['username']
        user = get_user_model().objects.exclude(pk=self.instance.pk).filter(username__iexact=username).first()
        if user == None:
            return username
        else:
            raise forms.ValidationError(f'Username "{username}" is already in use.')

    def clean_email(self):
        """ Convert all emails to lowercase befor saving """
        email = self.cleaned_data['email'].lower()
        try:
            user = get_user_model().objects.exclude(pk=self.instance.pk).get(email=email)
        except get_user_model().DoesNotExist:
            return email
        raise forms.ValidationError(f'Username "{email}" is already in use.')


class UpdateProfile(forms.ModelForm):
    picture = forms.ImageField(widget=forms.FileInput, required=False)

    class Meta:
        model = Profile
        fields = ['picture']
