from .models import Category, Tag

def layout_data(request):

    categories = Category.objects.all()
    cats_list = []
    for cat in categories:
        cats_list.append({
            'name': cat.name,
            'alias': cat.alias,
            'entries_num': cat.entry_set.count()
        })

    tags = Tag.objects.all()
    tags_list = []
    for tag in tags:
        tags_list.append({
            'name': tag.name,
            'alias': tag.alias,
            'entries_num': tag.entry_set.count()
        })

    return {
        'cats_list': cats_list,
        'tags_list': tags_list,
        'current_page': request.session.get('current_page', ''),
    }
