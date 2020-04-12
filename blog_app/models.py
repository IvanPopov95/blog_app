from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Article(models.Model):
    author = models.ForeignKey('auth.User', on_delete = models.CASCADE)
    title = models.CharField(max_length= 100)
    body = models.TextField()
    slug = models.SlugField(db_index=True, null=True)
    created = models.DateTimeField(default=timezone.now, editable=False)
    updated = models.DateTimeField(null=True, editable=False)

    def save(self, *args, **kwargs):
        if self.created < timezone.now():
            self.updated = timezone.now()
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail', args=[str(self.slug)])
    
    def like_count(self):
        return ArticleLikes.objects.filter(article=self).count()


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_posted = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.body


class ArticleLikes(models.Model):
    user = models.ForeignKey('auth.user', on_delete=models.CASCADE, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()