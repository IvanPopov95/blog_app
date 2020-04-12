from django import forms
from .models import Article, Comment, Profile
from django.contrib.auth.models import User

class CreateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'body', 'slug')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('location', )

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')