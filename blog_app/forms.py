from django import forms
from .models import Article, Comment

class CreateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'body', 'slug')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)