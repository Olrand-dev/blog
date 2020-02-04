from .models import Category

def layout_data(request):

    categories = Category.objects.all()
    cats_list = []
    for cat in categories:
        cats_list.append({
            'name': cat.name,
            'alias': cat.alias,
            'entries_num': cat.entry_set.count()
        })
    return {
        'cats_list': cats_list,
    }