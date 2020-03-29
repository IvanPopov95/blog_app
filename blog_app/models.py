from django.db import models
from django.utils import timezone
from django.urls import reverse

class Article(models.Model):
    author = models.ForeignKey('auth.User', on_delete = models.CASCADE)
    title = models.CharField(max_length= 100)
    body = models.TextField()
    slug = models.SlugField(db_index=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail', args=[str(self.slug)])    

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    author = models.ForeignKey('auth.User', on_delete = models.CASCADE, null=True)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.body