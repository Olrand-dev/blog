from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'base'

urlpatterns = [
    path('', views.index, name='index'),

    path('articles/article/<slug:entry_type>/<int:entry_id>/', views.show_entry_page, name='entry-page'),

    path('articles/all/', views.show_all_entries_list, name='all-list'),
    path('articles/category/<slug:cat_alias>/', views.show_cat_list, name='cat-list'),
    path('articles/tag/<slug:tag_alias>/', views.show_tag_list, name='tag-list'),
    path('articles/archive/<int:year>/', views.show_year_archive_list, name='year-archive'),
    path('articles/archive/<int:year>/<int:month>/', views.show_month_archive_list, name='month-archive'),
    path('articles/search/', views.show_search_list, name='search'),


    path('write-s-data', views.write_session_data, name="write-session-data"),
    path('get-user-data', views.get_user_data, name='get-user-data'),
    path('get-entries-list', views.get_entries_list, name='get-entries-list'),
    path('get-entry-list-options', views.get_entry_list_options, name='get-entry-list-options'),
    path('add-comment', views.add_comment, name='add-comment'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
