from django.shortcuts import render
from django.http import JsonResponse
from blog.utils import ApiResponse
from .models import Entry, Author, Article, VideoArticle

def index(request):
    return render(request, 'base/index.html')


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
    resp = ApiResponse()
    entries = Entry.objects.all()

    articles = list(Article.objects.all().values())
    video_articles = list(VideoArticle.objects.all().values())
    entries_data = articles + video_articles
    entries_data = sorted(entries_data, key=lambda i: i['pub_date'], reverse=True)

    for entry_data in entries_data:
        entry = entries.get(pk=entry_data['id'])
        author = Author.objects.get(pk=entry_data['author_id'])

        entry_data['category'] = entry.category.name
        entry_data['pub_date'] = entry.pub_date.strftime("%b %d, %Y")
        entry_data['author'] = f'{author.user.first_name} {author.user.last_name}'

    resp.data = entries_data
    return JsonResponse(resp.get_resp_data())
