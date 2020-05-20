from django import forms
from .models import Article, Comment, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

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

class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email")

    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
