import json
import datetime
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse
from django.templatetags.static import static
from blog.utils import ApiResponse, string_sanitize
from blog import const
from .models import Entry, Author, Article, VideoArticle, QuoteEntry, LinkEntry, Category, Tag, Comment


def index(request):

    request.session['current_page'] = 'home'
    return show_all_entries_list(request)


def show_all_entries_list(request):

    return render(request, 'base/entries-list.html', {
        'page_obj': get_paginated_entries_list(request, 'all'),
        'list_type': 'all',
    })


def show_cat_list(request, cat_alias):
    cat = Category.objects.get(alias=cat_alias)
    request.session['current_page'] = 'categories'

    return render(request, 'base/entries-list.html', {
        'page_obj': get_paginated_entries_list(request, 'cat', {'cat_alias': cat_alias}),
        'list_type': 'cat',
        'cat_name': cat.name,
    })


def show_tag_list(request, tag_alias):
    tag = Tag.objects.get(alias=tag_alias)
    request.session['current_page'] = 'tags'

    return render(request, 'base/entries-list.html', {
        'page_obj': get_paginated_entries_list(request, 'tag', {'tag_alias': tag_alias}),
        'list_type': 'tag',
        'tag_name': tag.name,
    })


def show_search_list(request):
    query = request.POST['query']

    return render(request, 'base/entries-list.html', {
        'page_obj': get_paginated_entries_list(
            request, 'search', {'search_query': query}
        ),
        'list_type': 'search',
        'search_query': query,
    })


def show_year_archive_list(request, year):

    return render(request, 'base/entries-list.html', {
        'page_obj': get_paginated_entries_list(request, 'year_archive', {'year': year}),
        'list_type': 'year_archive',
        'year': year,
    })


def show_month_archive_list(request, year, month):
    date = datetime.date(year, month, 1)

    return render(request, 'base/entries-list.html', {
        'page_obj': get_paginated_entries_list(
            request, 'month_archive', {'year': year, 'month': month}
        ),
        'list_type': 'month_archive',
        'year': year,
        'month': date.strftime("%B"),
    })


def show_entry_page(request, entry_type, entry_id):

    sort_type = request.session.get('sort_type', const.ENTRIES_SORT_TYPE)
    entry_data = get_entry_data_by_type(entry_type, entry_id)
    entry_data = get_entry_details(entry_data, sort_type, True)

    return render(request, 'base/entry-page.html', {
        'entry': entry_data
    })


def show_flat_page(request, page_alias):

    request.session['current_page'] = page_alias
    return render(request, f'base/{page_alias}.html', {})
    


def get_paginated_entries_list(request, list_type='all', options=None):

    sort_type = request.session.get('sort_type', const.ENTRIES_SORT_TYPE)
    entries_list = get_entries_list(list_type=list_type, sort_type=sort_type, options=options)

    per_page = request.session.get('per_page', request.GET.get('per_page', const.ENTRIES_PER_PAGE))
    page = request.GET.get('page', 1)
    page_obj = paginate(entries_list, page, per_page)

    return page_obj


def paginate(data_list, page=1, per_page=const.ENTRIES_PER_PAGE):

    paginator = Paginator(data_list, per_page)
    return paginator.get_page(page)


def get_entries_list(only_list=False, list_type='all', sort_type=const.ENTRIES_SORT_TYPE, options=None):

    if list_type == 'all':
        entries_data = Entry.objects.all()

    elif list_type == 'cat':
        cat = Category.objects.get(alias=options['cat_alias'])
        entries_data = cat.entry_set.all()

    elif list_type == 'tag':
        tag = Tag.objects.get(alias=options['tag_alias'])
        entries_data = tag.entry_set.all()

    elif list_type == 'search':
        query = options['search_query']
        entries_data = Entry.objects.filter(Q(header__search=query) | Q(text__search=query))

    elif list_type == 'year_archive':
        entries_data = Entry.objects.filter(pub_date__year=options['year'])

    elif list_type == 'month_archive':
        all_entries = Entry.objects.all()
        entries_data = filter(
            lambda e: e.pub_date.year == options['year'] and e.pub_date.month == options['month'], 
            all_entries
        )

    else:
        entries_data = []


    if sort_type == const.ENTRIES_SORT_TYPE_PUBDATE_ASC:
        entries_data = sorted(entries_data, key=lambda i: i.pub_date)
    elif sort_type == const.ENTRIES_SORT_TYPE_PUBDATE_DESC:
        entries_data = sorted(entries_data, key=lambda i: i.pub_date, reverse=True)

    if only_list or len(entries_data) == 0:
        return entries_data

    full_entries_data = []
    for entry_data in entries_data:
        full_entries_data.append(get_entry_details(entry_data))

    return full_entries_data


def get_entry_details(base_data, sort_type=const.ENTRIES_SORT_TYPE, full=False):

    entry_data = base_data
    entry_data.entry_type = get_entry_type(entry_data.id)
    entry_data = get_entry_data_by_type(entry_data.entry_type, entry_data.id)
    
    entry = Entry.objects.get(pk=entry_data.id)
    author = Author.objects.get(pk=entry_data.author_id)

    entry_data.category_name = entry.category.name
    entry_data.category_alias = entry.category.alias
    entry_data.author_name = f'{author.user.first_name} {author.user.last_name}'
    entry_data.excerpt = entry.text[:150]

    if full:
        entry_data.tags_list = entry_data.tags.all()

        all_entries = get_entries_list(list_type='all', sort_type=sort_type)
        all_entries = list(filter(lambda entry: entry.entry_type in ('standard', 'video'), all_entries))

        e_index = [x.id for x in all_entries].index(entry_data.id)
        if e_index > 0:
            entry_data.prev_entry = all_entries[e_index - 1]
        if e_index < (len(all_entries) - 1):
            entry_data.next_entry = all_entries[e_index + 1]

        cat = Category.objects.get(pk=entry_data.category_id)
        cat_entries = get_entries_list(
            list_type='cat', sort_type=sort_type, options={'cat_alias': cat.alias}
        )
        entry_data.related_entries = get_entry_related_entries(cat_entries, entry_data.id, 3)

        entry_data.comments_list = entry.comment_set.all()
        for comment in entry_data.comments_list:
            comment = get_comment_details(comment)

            comment.children = comment.replies.all()
            comment.child_count = comment.children.count()
            for c_comment in comment.children:
                c_comment = get_comment_details(c_comment)

    return entry_data


def get_entry_type(entry_id):

    if len(Article.objects.filter(pk=entry_id)) > 0:
        return 'standard'
    if len(VideoArticle.objects.filter(pk=entry_id)) > 0:
        return 'video'
    if len(QuoteEntry.objects.filter(pk=entry_id)) > 0:
        return 'quote'
    if len(LinkEntry.objects.filter(pk=entry_id)) > 0:
        return 'link'


def get_entry_data_by_type(entry_type, entry_id):
    entry_data = None

    if entry_type == 'standard':
        entry_data = Article.objects.get(pk=entry_id)
    elif entry_type == 'video':
        entry_data = VideoArticle.objects.get(pk=entry_id)
    elif entry_type == 'quote':
        entry_data = QuoteEntry.objects.get(pk=entry_id)
    elif entry_type == 'link':
        entry_data = LinkEntry.objects.get(pk=entry_id)

    return entry_data


def get_entry_related_entries(entries_list, main_id, num):

    def filter_list(entry):
        return entry.id != main_id and (entry.entry_type in ('standard', 'video'))

    entries_list = filter(filter_list, entries_list)
    return list(entries_list)[:num]


def write_session_data(request):
    resp = ApiResponse()
    data = json.loads(request.POST['data'])

    for item in data:
        request.session[item['key']] = item['value']

    return JsonResponse(resp.get_resp_data())


def get_entry_list_options(request):
    options = {
        'per_page': request.session.get('per_page', const.ENTRIES_PER_PAGE),
        'sort_type': request.session.get('sort_type', const.ENTRIES_SORT_TYPE),
    }

    resp = ApiResponse()
    resp.data = options
    return JsonResponse(resp.get_resp_data())


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


def get_comment_details(comment):
    guest_comment = comment.author is None
    if guest_comment:
        comment.author_name = comment.a_name
        comment.avatar_url = static('base/img/avatars/avatar.png')
    else:
        comment.author_name = f'{comment.author.user.first_name} {comment.author.user.last_name}'
        comment.avatar_url = comment.author.avatar.url

    return comment


def add_comment(request):
    form_data = json.loads(request.POST['form_data'])
    entry_id = int(request.POST['entry_id'])
    is_reply = int(request.POST['is_reply']) == 1
    reply_parent_id = int(request.POST['reply_parent_id'])
    resp = ApiResponse()

    entry = Entry.objects.get(pk=entry_id)
    name = string_sanitize(form_data['name'])
    email = string_sanitize(form_data['email'])
    message = string_sanitize(form_data['message'])

    comment = Comment(entry=entry, text=message, a_name=name, a_email=email)

    if is_reply:
        comment.parent = Comment.objects.get(pk=reply_parent_id)

    comment.save()
    return JsonResponse(resp.get_resp_data())


def send_message(request):

    resp = ApiResponse()
    return JsonResponse(resp.get_resp_data())
