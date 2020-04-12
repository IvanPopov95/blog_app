from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, UpdateView
from .models import Article, ArticleLikes, Profile, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import AccessMixin
from .forms import CreateArticleForm, CommentForm, UserForm, ProfileForm
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import messages


class ArticleListView(ListView):
    model = Article
    template_name = 'blog/articles.html'
    paginate_by = 3


def article_detail_view(request, slug):
    template_name = 'blog/detail.html'
    article = get_object_or_404(Article, slug=slug)
    comments = article.comments.filter()
    new_comment = None
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.article = article
            new_comment.author = request.user
            new_comment.save()
    else:
        form = CommentForm()
    return render(request, template_name,{'article' : article,
                                        'comments': comments, 
                                        'new_comment': new_comment, 
                                        'form': form})


@login_required
def like(request, slug):
        article = get_object_or_404(Article, slug=slug)
        like, created = ArticleLikes.objects.get_or_create(article=article, user=request.user)
        if not created:
            like.delete()
        return redirect('detail', slug=slug)


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('articles')
    else:
        form = UserCreationForm()
        context = {'form' : form}
        return render(request, 'registration/register.html', context)


@login_required
def create_article_view(request):
    form = CreateArticleForm(request.POST or None)
    if form.is_valid() and request.user:
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        form = CreateArticleForm()

    return render(request, 'blog/create_article.html', {'form' : form})


def delete_article_view(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if request.method == 'POST':
        article.delete()
        return redirect('articles')
    return render(request, "blog/delete_article.html", {"article": article})


class ArticleUpdateView(AccessMixin, UpdateView):
    template_name = 'blog/create_article.html'
    form_class = CreateArticleForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not self.request.user == self.get_object().author:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
    
    def get_object(self):
        slug = self.kwargs.get("slug")
        return get_object_or_404(Article, slug=slug)
     

class SearchView(ListView):
    model = Article
    template_name = 'blog/search.html'

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        lookups = (
            Q(author__username__icontains=query) |
            Q(title__icontains=query)
        )
        if query is not None:
            qs = super().get_queryset().filter(lookups).distinct()
            return qs
        qs = super().get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context


@login_required
def profile_view(request):
    template_name = 'blog/profile_page.html'
    user = request.user
    user_comments = Comment.objects.filter(author=user)
    user_articles = Article.objects.filter(author=user)
    user_likes = ArticleLikes.objects.filter(user=user)
    return render(request, template_name, {'user_comments': user_comments,
                                          'user_articles':  user_articles,
                                          'user_likes': user_likes})


@login_required
def update_profile_view(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('profile_page')
        else:
            messages.error(request, ('Please correct the error.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'blog/update_profile.html', {
                                            'user_form': user_form,
                                            'profile_form': profile_form})
