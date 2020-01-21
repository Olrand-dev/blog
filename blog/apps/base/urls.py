from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'base'

urlpatterns = [
    path('', views.index, name='index'),
    path('articles/<slug:entry_type>/<int:entry_id>/', views.show_entry_page, name='entry-page'),
    path('category/<slug:cat_alias>/', views.show_cat_list, name='cat-list'),
    path('tag/<slug:tag_alias>/', views.show_tag_list, name='tag-list'),
    path('archive/<int:year>/', views.show_year_archive, name='year-archive'),
    path('archive/<int:year>/<int:month>/', views.show_month_archive, name='month-archive'),


    path('get-user-data', views.get_user_data, name='get-user-data'),
    path('get-entries-list', views.get_entries_list, name='get-entries-list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
