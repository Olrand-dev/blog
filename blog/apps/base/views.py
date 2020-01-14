from itertools import chain
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import JsonResponse
from blog.utils import ApiResponse
from blog import const
from .models import Entry, Author, Article, VideoArticle

def index(request):
    entries_list = get_entries_list(request)

    per_page = request.GET.get('per_page', const.PER_PAGE)
    page = request.GET.get('page', 1)
    paginator = Paginator(entries_list, per_page)
    page_obj = paginator.get_page(page)

    return render(request, 'base/index.html', {
        'page_obj': page_obj
    })


def show_entry_page(request):
    pass


def show_cat_list(request):
    pass


def show_tag_list(request):
    pass


def show_year_archive(request):
    pass


def show_month_archive(request):
    pass





def get_user_data(request):
    user = request.user
    profile_data = None
    if hasattr(user, 'author'):
        profile_data = user.author

    data = {
        'user_auth': False,
    }
    resp = ApiResponse()

    if user.is_authenticated:
        if profile_data is not None:
            data['user_id'] = profile_data.pk
        data['user_auth'] = True
        data['user_login'] = user.username
        data['user_name'] = f'{user.first_name} {user.last_name}'

        user_groups = user.groups.all()
        if user_groups.count() > 0:
            data['user_group'] = user_groups[:1].get().name

    resp.data = data
    return JsonResponse(resp.get_resp_data())


def get_entries_list(request):

    entries = Entry.objects.all()

    articles = Article.objects.all()
    video_articles = VideoArticle.objects.all()
    entries_data = sorted(chain(articles, video_articles), key=lambda i: i.pub_date)

    for entry_data in entries_data:
        entry = entries.get(pk=entry_data.id)
        author = Author.objects.get(pk=entry_data.author_id)

        entry_data.category_name = entry.category.name
        entry_data.pub_date_formated = entry.pub_date.strftime("%b %d, %Y")
        entry_data.author_name = f'{author.user.first_name} {author.user.last_name}'
        entry_data.excerpt = entry_data.text[:150]
        entry_data.image_thumb_link = entry.image_thumb.url
        entry_data.entry_page_link = f"articles/{entry_data.entry_type}/{entry_data.id}/"
        entry_data.cat_list_link = f"category/{entry.category.alias}/"
        entry_data.month_archive_link = f"archive/{entry.pub_date.year}/{entry.pub_date.month}/"

    return entries_data
