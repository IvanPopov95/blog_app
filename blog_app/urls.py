from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticleListView.as_view(), name = 'articles'),
    path('register/', views.register, name='register'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('create_article/', views.create_article_view, name = 'create'),
    path('<str:slug>/', views.article_detail_view, name='detail'),
    path('<str:slug>/like/', views.like, name='like'),
    path('<str:slug>/update/', views.ArticleUpdateView.as_view(), name='update'),
    path('<str:slug>/delete/', views.delete_article_view, name='delete'),
]