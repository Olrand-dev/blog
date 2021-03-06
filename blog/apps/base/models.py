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
    alias = models.CharField('alias', max_length=100)
    desc = models.TextField('description', blank=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return f'{self.name}'


class Tag(models.Model):
    name = models.CharField('tag name', max_length=50)
    alias = models.CharField('alias', max_length=100)

    def __str__(self):
        return f'{self.name}'
    


class Entry(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    pub_date = models.DateTimeField('publication date', auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    header = models.CharField('header', max_length=150)
    text = models.TextField('text', blank=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        f_name = self.author.user.first_name
        l_name = self.author.user.last_name
        return f'{self.header} - {f_name} {l_name} - {self.pub_date.strftime("%Y-%m-%d %H:%M:%S")}'


class Article(Entry):
    entry_type = models.CharField(max_length=50, editable=False, default='standard')
    image_thumb = models.ImageField('thumbnail image', upload_to='articles/thumbs/standard', blank=True)
    image = models.ImageField('full image', upload_to='articles/full-images/standard', blank=True)


class VideoArticle(Entry):
    entry_type = models.CharField(max_length=50, editable=False, default='video')
    image_thumb = models.ImageField('thumbnail image', upload_to='articles/thumbs/video', blank=True)
    video_url = models.CharField('video link', max_length=200)


class QuoteEntry(Entry):
    entry_type = models.CharField(max_length=50, editable=False, default='quote')
    cite = models.CharField('cite', max_length=50)

    class Meta:
        verbose_name_plural = 'quote entries'


class LinkEntry(Entry):
    entry_type = models.CharField(max_length=50, editable=False, default='link')
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
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True)
    a_name = models.CharField('author name', max_length=150, blank=True)
    a_email = models.CharField('author email', max_length=100, blank=True)

    def __str__(self):
        guest_comment = self.author is None
        p_date = self.pub_date.strftime("%Y-%m-%d %H:%M:%S")

        if guest_comment:
            return f'{self.a_name}, {self.a_email} - {p_date}'
        else:
            return f'{self.author.user.first_name} {self.author.user.last_name} - {p_date}'


class Search(models.Lookup):
    lookup_name = 'search'

    def as_mysql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return 'MATCH (%s) AGAINST (%s IN BOOLEAN MODE)' % (lhs, rhs), params

models.CharField.register_lookup(Search)
models.TextField.register_lookup(Search)
