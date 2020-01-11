from django.contrib import admin
from .models import Article, Category, Tag, VideoArticle, QuoteEntry, LinkEntry, Author

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Article)
admin.site.register(VideoArticle)
admin.site.register(QuoteEntry)
admin.site.register(LinkEntry)
admin.site.register(Author)
