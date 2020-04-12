from django.contrib import admin
from .models import Article, Comment, ArticleLikes, Profile

admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(ArticleLikes)
admin.site.register(Profile)
