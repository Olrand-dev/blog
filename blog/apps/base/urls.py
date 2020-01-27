from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'base'

urlpatterns = [
    path('', views.index, name='index'),
    path('articles/all/<int:per_page>/<int:page>/', views.show_all_entries_list, name='entry-page'),
    path('articles/article/<slug:entry_type>/<int:entry_id>/', views.show_entry_page, name='entry-page'),
    path('articles/category/<slug:cat_alias>/<int:per_page>/<int:page>/', views.show_cat_list, name='cat-list'),
    path('articles/tag/<slug:tag_alias>/<int:per_page>/<int:page>/', views.show_tag_list, name='tag-list'),
    path('articles/archive/<int:year>/<int:per_page>/<int:page>/', views.show_year_archive_list, name='year-archive'),
    path('articles/archive/<int:year>/<int:month>/<int:per_page>/<int:page>/', views.show_month_archive_list, name='month-archive'),
    path('articles/search/<int:per_page>/<int:page>/', views.show_search_list, name='search'),


    path('get-user-data', views.get_user_data, name='get-user-data'),
    path('get-entries-list', views.get_entries_list, name='get-entries-list'),
    path('add-comment', views.add_comment, name='add-comment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
