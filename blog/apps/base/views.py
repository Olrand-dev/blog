from itertools import chain
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import JsonResponse
from blog.utils import ApiResponse
from blog import const
from .models import Entry, Author, Article, VideoArticle, Category, Tag

def index(request):
    entries_list = get_entries_list()

    per_page = request.GET.get('per_page', const.PER_PAGE)
    page = request.GET.get('page', 1)
    page_obj = paginate(entries_list, page, per_page)

    return render(request, 'base/index.html', {
        'page_obj': page_obj
    })


def paginate(entries_list, page=1, per_page=const.PER_PAGE):

    paginator = Paginator(entries_list, per_page)
    return paginator.get_page(page)


def get_entry_type(entry_id):
    entry_type = 'standard'

    if len(VideoArticle.objects.filter(pk=entry_id)) > 0:
        entry_type = 'video'

    return entry_type


def get_entry_data_by_type(entry_type, entry_id):
    entry_data = None

    if entry_type == 'standard':
        entry_data = Article.objects.get(pk=entry_id)
    elif entry_type == 'video':
        entry_data = VideoArticle.objects.get(pk=entry_id)
    
    return entry_data


def show_entry_page(request, entry_type, entry_id):
    
    entry_data = get_entry_data_by_type(entry_type, entry_id)
    entry_data = get_entry_details(entry_data, True)

    return render(request, 'base/entry-page.html', {
        'entry': entry_data
    })


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


def get_entries_list(only_list=False):

    articles = Article.objects.all()
    video_articles = VideoArticle.objects.all()
    entries_data = sorted(chain(articles, video_articles), key=lambda i: i.pub_date)
    if only_list:
        return entries_data

    for entry_data in entries_data:
        entry_data = get_entry_details(entry_data)

    return entries_data


def get_cat_entries_list(cat_id, only_list=False):
    category = Category.objects.get(pk=cat_id)
    entries = sorted(category.entry_set.all(), key=lambda i: i.pub_date)
    for entry_data in entries:
        entry_data.entry_type = get_entry_type(entry_data.id)

    if only_list:
        return entries
    
    for entry_data in entries:
        entry_data = get_entry_details(entry_data)

    return entries


def get_entry_details(base_data, full=False):

    entry_data = base_data
    entry = Entry.objects.get(pk=entry_data.id)
    author = Author.objects.get(pk=entry_data.author_id)

    entry_data.category_name = entry.category.name
    entry_data.category_alias = entry.category.alias
    entry_data.author_name = f'{author.user.first_name} {author.user.last_name}'
    entry_data.excerpt = entry_data.text[:150]

    if full:
        entry_data.tags_list = entry_data.tags.all()

        all_entries = get_entries_list(True)
        e_index = [x.id for x in all_entries].index(entry_data.id)
        if e_index > 0:
            entry_data.prev_entry = all_entries[e_index - 1]
        if e_index < (len(all_entries) - 1):
            entry_data.next_entry = all_entries[e_index + 1]

        cat_entries = get_cat_entries_list(entry_data.category_id, True)
        entry_data.related_entries = cat_entries[:3]

        entry_data.comments_list = entry.comment_set.all()
        for comment in entry_data.comments_list:
            comment.children = comment.replies.all()
            comment.child_count = comment.children.count()
            comment.author_name = f'{comment.author.user.first_name} {comment.author.user.last_name}'

    return entry_data
