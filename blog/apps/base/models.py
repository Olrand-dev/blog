from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField('country', max_length=50, blank=True)
    state = models.CharField('state', max_length=150, blank=True)
    city = models.CharField('city', max_length=50, blank=True)


class Category(models.Model):
    name = models.CharField('category name', max_length=100)
    desc = models.TextField('description', blank=True)


class Tag(models.Model):
    name = models.CharField('tag name', max_length=50)


class Entry(models.Model):
    header = models.CharField('header', max_length=150)
    pub_date = models.DateTimeField('publication date', auto_now_add=True)
    text = models.TextField('text')
    image_thumb = models.ImageField('thumbnail image', upload_to='articles/thumbs/')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)


class Article(Entry):
    image = models.ImageField('full image', upload_to='articles/full-images/')

class VideoArticle(Entry):
    video_url = models.CharField('video link', max_length=200)


class QuoteEntry(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    text = models.TextField('text')
    cite = models.CharField('cite', max_length=50)


class LinkEntry(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    desc = models.CharField('link description', max_length=150, blank=True)
    url = models.CharField('link', max_length=200)


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name="replies",
        related_query_name="reply"
    )
    pub_date = models.DateTimeField('publication date', auto_now_add=True)
    text = models.TextField('text')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
