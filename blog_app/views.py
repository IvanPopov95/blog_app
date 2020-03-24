from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, UpdateView
from .models import Article
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import AccessMixin
from .forms import CreateArticleForm, CommentForm
from django.db.models import Q

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