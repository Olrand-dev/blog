from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField('country', max_length=50, blank=True)
    state = models.CharField('state', max_length=150, blank=True)
    city = models.CharField('city', max_length=50, blank=True)
    avatar = models.ImageField('avatar', upload_to='users/avatars/', blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Category(models.Model):
    name = models.CharField('category name', max_length=100)
    alias = models.CharField('alias', max_length=100, null=True)
    desc = models.TextField('description', blank=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return f'{self.name}'


class Tag(models.Model):
    name = models.CharField('tag name', max_length=50)
    alias = models.CharField('alias', max_length=100, null=True)

    def __str__(self):
        return f'{self.name}'


class BaseEntry(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('publication date', auto_now_add=True)

    class Meta:
        abstract = True


class Entry(BaseEntry):
    header = models.CharField('header', max_length=150)
    text = models.TextField('text')
    image_thumb = models.ImageField('thumbnail image', upload_to='articles/thumbs/', blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return f'{self.header} - {self.author.user.first_name} {self.author.user.last_name} - {self.pub_date.strftime("%Y-%m-%d %H:%M:%S")}'


class SpecialEntry(BaseEntry):
    header = models.CharField('header', max_length=150)

    class Meta:
        verbose_name_plural = 'special entries'

    def __str__(self):
        return f'{self.header} - {self.pub_date.strftime("%Y-%m-%d %H:%M:%S")}'


class Article(Entry):
    entry_type = models.CharField(max_length=50, editable=False, default='standard')
    image = models.ImageField('full image', upload_to='articles/full-images/', blank=True)


class VideoArticle(Entry):
    entry_type = models.CharField(max_length=50, editable=False, default='video')
    video_url = models.CharField('video link', max_length=200)


class QuoteEntry(SpecialEntry):
    text = models.TextField('text')
    cite = models.CharField('cite', max_length=50)

    class Meta:
        verbose_name_plural = 'quote entries'


class LinkEntry(SpecialEntry):
    desc = models.CharField('link description', max_length=150, blank=True)
    url = models.CharField('link', max_length=200)

    class Meta:
        verbose_name_plural = 'link entries'


class Comment(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name="replies",
        related_query_name="reply",
        null=True,
        blank=True
    )
    pub_date = models.DateTimeField('publication date', auto_now_add=True)
    text = models.TextField('text')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author.user.first_name} {self.author.user.last_name} - {self.pub_date.strftime("%Y-%m-%d %H:%M:%S")}'
